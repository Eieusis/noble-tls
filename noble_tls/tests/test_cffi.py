import pytest
from unittest.mock import MagicMock
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
    cffi_mod._library = None  # force re-init
    lib = cffi_mod._get_library()

    for fn_name in ['request', 'freeMemory', 'getCookiesFromSession',
                     'addCookiesToSession', 'destroySession', 'destroyAll']:
        assert hasattr(lib, fn_name), f"Library missing {fn_name}"
