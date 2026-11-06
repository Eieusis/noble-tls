import asyncio
import time

import pytest

from noble_tls import Client, Session
from noble_tls.exceptions.exceptions import TLSClientException


@pytest.mark.asyncio
async def test_bundled_native_preserves_body_header_order_and_cookie_state():
    requests = []

    async def handle(reader, writer):
        try:
            headers = await reader.readuntil(b"\r\n\r\n")
            lines = headers.decode().split("\r\n")
            values = dict(line.split(": ", 1) for line in lines[1:] if ": " in line)
            length = next((int(v) for k, v in values.items() if k.lower() == "content-length"), 0)
            body = await reader.readexactly(length)
            requests.append((lines, body))
            writer.write(b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\nSet-Cookie: sid=fresh; Path=/\r\nConnection: close\r\n\r\nok")
            await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()

    server = await asyncio.start_server(handle, "127.0.0.1", 0)
    url = f"http://127.0.0.1:{server.sockets[0].getsockname()[1]}/"
    session = Session(client=Client.CHROME_152, header_order=["x-second", "x-first", "cookie"],
                      force_http1=True, disable_http3=True)
    try:
        response = await session.post(url, headers={"x-first": "one", "x-second": "two", "cookie": "manual=value"},
                                      data=b"\x00\xffnative", timeout_seconds=2)
        assert response.status_code == 200
        lines, body = requests[0]
        names = [line.split(":", 1)[0].lower() for line in lines[1:] if ":" in line]
        assert names.index("x-second") < names.index("x-first") < names.index("cookie")
        assert "cookie: manual=value" in [line.lower() for line in lines]
        assert body == b"\x00\xffnative"
        assert any(c["name"] == "sid" and c["value"] == "fresh" for c in await session.get_cookies(url))
        await session.get(url, timeout_seconds=2)
        assert any("sid=fresh" in line for line in requests[1][0])
    finally:
        await session.close()
        server.close()
        await server.wait_closed()


@pytest.mark.asyncio
async def test_bundled_native_bounds_stalled_proxy_connect():
    connected, disconnected = asyncio.Event(), asyncio.Event()

    async def handle(reader, writer):
        try:
            await reader.readuntil(b"\r\n\r\n")
            connected.set()
            await reader.read()
        finally:
            writer.close()
            await writer.wait_closed()
            disconnected.set()

    server = await asyncio.start_server(handle, "127.0.0.1", 0)
    proxy = f"http://127.0.0.1:{server.sockets[0].getsockname()[1]}"
    session = Session(client=Client.CHROME_152, disable_http3=True)
    started = time.monotonic()
    try:
        with pytest.raises(TLSClientException):
            await asyncio.wait_for(session.get("https://example.com/", proxy=proxy,
                                               timeout_milliseconds=100), 3)
        assert connected.is_set() and time.monotonic() - started < 2
        await asyncio.wait_for(disconnected.wait(), 2)
    finally:
        await session.close()
        server.close()
        await server.wait_closed()
