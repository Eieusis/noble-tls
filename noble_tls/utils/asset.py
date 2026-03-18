import ctypes
import os
import platform
import sys

try:
    import distro
except ImportError:
    distro = None

# Hardcoded binary name prefix -- change this to match your compiled library name
BINARY_PREFIX = 'tls-client'


def root_dir() -> str:
    """Return the noble_tls package root directory."""
    current_file_path = os.path.abspath(__file__)
    current_dir_path = os.path.dirname(current_file_path)
    return os.path.dirname(current_dir_path)


def get_system_platform() -> str:
    """Return the current sys.platform string."""
    return sys.platform


def get_distro() -> str:
    """Return the Linux distribution ID, or empty string if unavailable."""
    if distro is not None:
        return distro.id()
    return ""


def generate_asset_name(custom_part: str = BINARY_PREFIX) -> str:
    """
    Generates a platform-specific binary filename for the bundled TLS library.

    No version suffix -- binaries are shipped directly in noble_tls/dependencies/.

    Expected naming convention per platform:
        macOS ARM64:  tls-client-darwin-arm64.dylib
        macOS x86_64: tls-client-darwin-amd64.dylib
        Linux x86_64: tls-client-linux-amd64.so
        Linux ARM64:  tls-client-linux-arm64.so
        Linux Ubuntu: tls-client-linux-ubuntu-amd64.so
        Windows 64:   tls-client-windows-64.dll

    :param custom_part: Prefix of the binary filename, e.g. 'tls-client'
    :return: Formatted binary filename string
    """
    system_os = platform.system().lower()
    architecture = platform.machine().lower()
    sys_platform = get_system_platform()

    if sys_platform == 'darwin':
        file_extension = '.dylib'
        asset_arch = 'arm64' if architecture == "arm64" else 'amd64'
    elif sys_platform in ('win32', 'cygwin'):
        file_extension = '.dll'
        asset_arch = '64' if 8 == ctypes.sizeof(ctypes.c_voidp) else '32'
    else:
        file_extension = '.so'

        if architecture == "aarch64":
            asset_arch = 'arm64'
        elif "x86" in architecture:
            asset_arch = 'amd64'
        else:
            asset_arch = 'amd64'

        if system_os == 'linux':
            distro_name = get_distro()
            if distro_name.lower() in {"ubuntu", "debian"}:
                system_os = f"{system_os}-ubuntu"

    return f"{custom_part}-{system_os}-{asset_arch}{file_extension}"


if __name__ == "__main__":
    asset_name = generate_asset_name()
    print(f">> Expected binary name: {asset_name}")
