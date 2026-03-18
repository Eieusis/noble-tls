import pytest
from unittest.mock import MagicMock

from ..exceptions.exceptions import TLSClientException
from ..updater.file_fetch import ensure_binary_exists


def test_ensure_binary_exists_found(mocker):
    """Returns the asset name when the binary file is present."""
    mocker.patch('noble_tls.updater.file_fetch.generate_asset_name', return_value='tls-client-darwin-arm64.dylib')
    mocker.patch('os.path.isdir', return_value=True)
    mocker.patch('os.path.isfile', return_value=True)

    asset = ensure_binary_exists()
    assert asset == 'tls-client-darwin-arm64.dylib'


def test_ensure_binary_exists_missing(mocker):
    """Raises TLSClientException with helpful message when binary is missing."""
    mocker.patch('noble_tls.updater.file_fetch.generate_asset_name', return_value='tls-client-darwin-arm64.dylib')
    mocker.patch('os.path.isdir', return_value=True)
    mocker.patch('os.path.isfile', return_value=False)

    with pytest.raises(TLSClientException, match="TLS binary not found"):
        ensure_binary_exists()


def test_ensure_binary_creates_deps_dir(mocker):
    """Creates the dependencies directory if it doesn't exist."""
    mocker.patch('noble_tls.updater.file_fetch.generate_asset_name', return_value='tls-client-linux-amd64.so')
    mocker.patch('os.path.isdir', return_value=False)
    mock_makedirs = mocker.patch('os.makedirs')
    mocker.patch('os.path.isfile', return_value=True)

    ensure_binary_exists()
    mock_makedirs.assert_called_once()
