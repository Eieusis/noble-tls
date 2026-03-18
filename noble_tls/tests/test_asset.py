import pytest
from noble_tls.utils.asset import root_dir, generate_asset_name


def test_root_dir():
    expected_part = 'noble_tls'
    assert root_dir().endswith(expected_part)


def test_generate_asset_name_linux_amd64(mocker):
    mocker.patch('noble_tls.utils.asset.get_system_platform', return_value='linux')
    mocker.patch('platform.machine', return_value='x86_64')
    mocker.patch('platform.system', return_value='Linux')
    mocker.patch('noble_tls.utils.asset.get_distro', return_value='')
    mocker.patch('ctypes.sizeof', return_value=8)
    assert generate_asset_name() == 'tls-client-linux-amd64.so'


def test_generate_asset_name_ubuntu_amd64(mocker):
    mocker.patch('noble_tls.utils.asset.get_system_platform', return_value='linux')
    mocker.patch('noble_tls.utils.asset.get_distro', return_value='ubuntu')
    mocker.patch('platform.machine', return_value='x86_64')
    mocker.patch('platform.system', return_value='Linux')
    assert generate_asset_name() == 'tls-client-linux-ubuntu-amd64.so'


def test_generate_asset_name_windows_x86(mocker):
    mocker.patch('noble_tls.utils.asset.get_system_platform', return_value='win32')
    mocker.patch('platform.system', return_value='Windows')
    mocker.patch('platform.machine', return_value='i686')
    mocker.patch('ctypes.sizeof', return_value=4)
    assert generate_asset_name() == 'tls-client-windows-32.dll'


def test_generate_asset_name_macos_arm64(mocker):
    mocker.patch('noble_tls.utils.asset.get_system_platform', return_value='darwin')
    mocker.patch('platform.system', return_value='Darwin')
    mocker.patch('platform.machine', return_value='arm64')
    assert generate_asset_name() == 'tls-client-darwin-arm64.dylib'


def test_generate_asset_name_unknown_architecture(mocker):
    mocker.patch('noble_tls.utils.asset.get_system_platform', return_value='linux')
    mocker.patch('platform.system', return_value='Linux')
    mocker.patch('platform.machine', return_value='unknown_arch')
    mocker.patch('noble_tls.utils.asset.get_distro', return_value='')
    mocker.patch('ctypes.sizeof', return_value=8)
    assert generate_asset_name() == 'tls-client-linux-amd64.so'
