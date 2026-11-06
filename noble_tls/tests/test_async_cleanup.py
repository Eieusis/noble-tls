import asyncio
from concurrent.futures import ThreadPoolExecutor
import threading

import pytest

from noble_tls import Session


RESPONSE = b'{"id":"response-id","status":200,"body":"OK","headers":{},"success":true,"cookies":[]}'


@pytest.mark.asyncio
async def test_completed_request_does_not_queue_cleanup_behind_unrelated_io(mocker):
    loop = asyncio.get_running_loop()
    executor = ThreadPoolExecutor(max_workers=1)
    loop.set_default_executor(executor)
    entered, busy = asyncio.Event(), asyncio.Event()
    release_request, release_busy = threading.Event(), threading.Event()

    def request(payload):
        loop.call_soon_threadsafe(entered.set)
        release_request.wait(5)
        return RESPONSE

    def unrelated_io():
        loop.call_soon_threadsafe(busy.set)
        release_busy.wait(5)

    mocker.patch('noble_tls.sessions.request', side_effect=request)
    free = mocker.patch('noble_tls.sessions.free_memory')
    task = asyncio.create_task(Session().get('https://example.com/'))
    try:
        await asyncio.wait_for(entered.wait(), 1)
        other = loop.run_in_executor(None, unrelated_io)
        release_request.set()
        await asyncio.wait_for(busy.wait(), 1)
        response = await asyncio.wait_for(asyncio.shield(task), .2)
        assert response.status_code == 200
        free.assert_called_once_with(b'response-id')
    finally:
        release_request.set()
        release_busy.set()
        await asyncio.gather(task, return_exceptions=True)
        executor.shutdown(wait=True)


@pytest.mark.asyncio
@pytest.mark.parametrize('native,method,args', [
    ('request', 'get', ('https://example.com/',)),
    ('destroy_session', 'close', ()),
    ('destroy_all', 'close_all', ()),
    ('get_cookies_from_session', 'get_cookies', ('https://example.com/',)),
    ('add_cookies_to_session', 'add_cookies', ('https://example.com/', [])),
])
async def test_cancelled_awaiter_still_frees_native_response(mocker, native, method, args):
    loop = asyncio.get_running_loop()
    entered, freed = asyncio.Event(), asyncio.Event()
    release = threading.Event()

    def call(*args):
        loop.call_soon_threadsafe(entered.set)
        release.wait(5)
        return RESPONSE

    mocker.patch('noble_tls.sessions.' + native, side_effect=call)
    free = mocker.patch('noble_tls.sessions.free_memory', side_effect=lambda value: loop.call_soon_threadsafe(freed.set))
    task = asyncio.create_task(getattr(Session(), method)(*args))
    try:
        await asyncio.wait_for(entered.wait(), 1)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        release.set()
        await asyncio.wait_for(freed.wait(), 1)
        free.assert_called_once_with(b'response-id')
    finally:
        release.set()
        await asyncio.gather(task, return_exceptions=True)
