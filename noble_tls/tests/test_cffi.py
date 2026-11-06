import pytest
from unittest.mock import MagicMock
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import threading
from ..c.cffi import initialize_library


def test_initialize_library(mocker):
    """initialize_library loads the shared library via ctypes."""
    mocker.patch('noble_tls.updater.file_fetch.ensure_binary_exists', return_value='some_asset')
    mocker.patch('ctypes.cdll.LoadLibrary', return_value=MagicMock())
    library = initialize_library()
    assert library is not None


def test_library_bindings_registered(mocker):
    """All 6 CFFI functions get their argtypes/restype set on first load."""
    mock_lib = MagicMock()
    mocker.patch('noble_tls.updater.file_fetch.ensure_binary_exists', return_value='some_asset')
    mocker.patch('ctypes.cdll.LoadLibrary', return_value=mock_lib)

    import noble_tls.c.cffi as cffi_mod
    mocker.patch.object(cffi_mod, '_library', None)  # force re-init, restore after the test
    lib = cffi_mod._get_library()

    for fn_name in ['request', 'freeMemory', 'getCookiesFromSession',
                     'addCookiesToSession', 'destroySession', 'destroyAll']:
        assert hasattr(lib, fn_name), f"Library missing {fn_name}"
    assert lib.freeMemory.restype is None


def test_concurrent_first_calls_cannot_observe_unconfigured_bindings(mocker):
    import noble_tls.c.cffi as cffi_mod
    configuring, release, second_started = threading.Event(), threading.Event(), threading.Event()

    class BlockingFunction:
        def __setattr__(self, name, value):
            if name == 'argtypes':
                configuring.set()
                assert release.wait(5)
            object.__setattr__(self, name, value)

    library = MagicMock()
    library.request = BlockingFunction()
    initialize = mocker.patch.object(cffi_mod, 'initialize_library', return_value=library)
    mocker.patch.object(cffi_mod, '_library', None)

    def second_call():
        second_started.set()
        return cffi_mod._get_library()

    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(cffi_mod._get_library)
        try:
            assert configuring.wait(1)
            second = pool.submit(second_call)
            assert second_started.wait(1)
            with pytest.raises(TimeoutError):
                second.result(timeout=.1)
        finally:
            release.set()
        assert first.result(timeout=1) is second.result(timeout=1) is library
    initialize.assert_called_once()
    assert library.freeMemory.restype is None
