"""
ctypes wrapper around the bundled TLS shared library.

The binary must already exist in noble_tls/dependencies/ -- see
``noble_tls.updater.file_fetch.ensure_binary_exists`` for the expected
naming convention.
"""

import ctypes
import os

from noble_tls.exceptions.exceptions import TLSClientException
from noble_tls.updater.file_fetch import ensure_binary_exists
from noble_tls.utils.asset import root_dir


def initialize_library():
    """
    Load the bundled TLS shared library via ctypes.

    :return: Loaded ctypes library object.
    :raises TLSClientException: If the binary is missing or fails to load.
    """
    try:
        asset_name = ensure_binary_exists()
        library_path = os.path.join(root_dir(), "dependencies", asset_name)
        library = ctypes.cdll.LoadLibrary(library_path)
        return library
    except TLSClientException:
        raise
    except OSError as e:
        msg = f"Failed to load the TLS library: {e}"
        if os.name == "darwin":
            msg += (
                " — If you're on macOS, allow the library in "
                "System Preferences > Privacy & Security > General."
            )
        raise TLSClientException(msg)


_library = None


def _get_library():
    """Return the cached library singleton, initialising on first call."""
    global _library
    if _library is None:
        _library = initialize_library()

        _library.request.argtypes = [ctypes.c_char_p]
        _library.request.restype = ctypes.c_char_p

        _library.freeMemory.argtypes = [ctypes.c_char_p]
        _library.freeMemory.restype = ctypes.c_char_p

        _library.getCookiesFromSession.argtypes = [ctypes.c_char_p]
        _library.getCookiesFromSession.restype = ctypes.c_char_p

        _library.addCookiesToSession.argtypes = [ctypes.c_char_p]
        _library.addCookiesToSession.restype = ctypes.c_char_p

        _library.destroySession.argtypes = [ctypes.c_char_p]
        _library.destroySession.restype = ctypes.c_char_p

        _library.destroyAll.argtypes = []
        _library.destroyAll.restype = ctypes.c_char_p

    return _library


def request(payload: bytes) -> ctypes.c_char_p:
    """Send a TLS request payload and return the raw response pointer."""
    return _get_library().request(payload)


def free_memory(response_id: bytes) -> ctypes.c_char_p:
    """Free memory associated with a previous response."""
    return _get_library().freeMemory(response_id)


def get_cookies_from_session(payload: bytes) -> ctypes.c_char_p:
    """Retrieve cookies for a session."""
    return _get_library().getCookiesFromSession(payload)


def add_cookies_to_session(payload: bytes) -> ctypes.c_char_p:
    """Add cookies to a session."""
    return _get_library().addCookiesToSession(payload)


def destroy_session(payload: bytes) -> ctypes.c_char_p:
    """Destroy a single TLS session."""
    return _get_library().destroySession(payload)


def destroy_all() -> ctypes.c_char_p:
    """Destroy all active TLS sessions."""
    return _get_library().destroyAll()
