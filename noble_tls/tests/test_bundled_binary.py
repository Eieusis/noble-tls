"""
Integration tests verifying that noble-tls loads the bundled binary
from noble_tls/dependencies/ and never attempts any remote downloads.
"""

import os
import ctypes

import pytest

from ..utils.asset import generate_asset_name, root_dir, BINARY_PREFIX
from ..updater.file_fetch import ensure_binary_exists
from ..c.cffi import initialize_library
from ..sessions import Session
from ..utils.identifiers import Client


class TestBundledBinaryExists:
    """Verify the correct binary file is present in dependencies/."""

    def test_asset_name_matches_platform(self):
        """generate_asset_name() produces a name without a version suffix."""
        name = generate_asset_name()
        assert name.startswith(BINARY_PREFIX)
        parts = name.rsplit(".", 1)
        stem = parts[0]  # e.g. tls-client-darwin-arm64
        ext = parts[1]   # e.g. dylib
        assert ext in ("dylib", "so", "dll"), f"Unexpected extension: {ext}"
        # Should NOT contain a semver-like segment (e.g. 1.14.0)
        import re
        assert not re.search(r"\d+\.\d+", stem), \
            f"Asset name appears to contain a version: {name}"

    def test_binary_file_exists_on_disk(self):
        """The expected binary is physically present in dependencies/."""
        asset_name = generate_asset_name()
        deps_dir = os.path.join(root_dir(), "dependencies")
        asset_path = os.path.join(deps_dir, asset_name)
        assert os.path.isfile(asset_path), \
            f"Binary not found at {asset_path}"

    def test_ensure_binary_exists_returns_name(self):
        """ensure_binary_exists() succeeds and returns the asset filename."""
        name = ensure_binary_exists()
        assert name == generate_asset_name()


class TestBinaryLoadsCorrectly:
    """Verify the shared library loads and exports the expected C symbols."""

    def test_library_initializes(self):
        """initialize_library() loads the .dylib/.so without errors."""
        lib = initialize_library()
        assert lib is not None

    def test_library_exports_all_symbols(self):
        """The loaded library exposes every C function noble-tls calls."""
        lib = initialize_library()
        required_symbols = [
            "request",
            "freeMemory",
            "getCookiesFromSession",
            "addCookiesToSession",
            "destroySession",
            "destroyAll",
        ]
        for sym in required_symbols:
            assert hasattr(lib, sym), f"Library missing exported symbol: {sym}"


class TestNoRemoteDownloads:
    """Confirm that the download mechanism has been fully removed."""

    def test_file_fetch_has_no_download_functions(self):
        """The updater module no longer exposes download/update functions."""
        from ..updater import file_fetch
        assert not hasattr(file_fetch, "download_if_necessary")
        assert not hasattr(file_fetch, "update_if_necessary")
        assert not hasattr(file_fetch, "get_latest_release")
        assert not hasattr(file_fetch, "download_and_save_asset")

    def test_no_httpx_dependency(self):
        """httpx is no longer imported anywhere in noble_tls."""
        import importlib
        import sys
        noble_modules = [
            key for key in sys.modules
            if key.startswith("noble_tls")
        ]
        for mod_name in noble_modules:
            mod = sys.modules[mod_name]
            if mod is None:
                continue
            mod_source = getattr(mod, "__file__", "") or ""
            if mod_source:
                assert "httpx" not in dir(mod), \
                    f"httpx found in {mod_name}"

    def test_no_version_file_needed(self):
        """The .version file is no longer required or referenced."""
        version_path = os.path.join(root_dir(), "dependencies", ".version")
        # It's fine if it doesn't exist; the point is we don't need it
        from ..updater import file_fetch
        assert not hasattr(file_fetch, "read_version_info")


@pytest.mark.asyncio
class TestEndToEnd:
    """Make a real HTTPS request through the bundled binary."""

    async def test_real_https_request(self):
        """Perform an actual GET request to verify the full stack works."""
        session = Session(
            client=Client.CHROME_133,
            random_tls_extension_order=True,
        )
        res = await session.get("https://tls.peet.ws/api/all")
        assert res.status_code == 200, \
            f"Expected 200, got {res.status_code}: {res.text[:200]}"
        body = res.json()
        assert "tls" in body, "Response missing 'tls' key"
        assert "ip" in body, "Response missing 'ip' key"
        await session.close()
