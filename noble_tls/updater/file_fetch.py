"""
Binary management for noble-tls.

Binaries are bundled directly in noble_tls/dependencies/ -- no remote downloads.
Place your compiled TLS shared library in that directory using the platform-specific
naming convention produced by ``generate_asset_name()``  (see noble_tls/utils/asset.py).
"""

import os

from noble_tls.utils.asset import generate_asset_name, root_dir
from noble_tls.exceptions.exceptions import TLSClientException

root_directory = root_dir()


def ensure_binary_exists() -> str:
    """
    Verify that the expected TLS binary is present in the dependencies folder.

    :return: The binary filename.
    :raises TLSClientException: If the binary is missing.
    """
    asset_name = generate_asset_name()
    deps_dir = os.path.join(root_directory, "dependencies")
    asset_path = os.path.join(deps_dir, asset_name)

    if not os.path.isdir(deps_dir):
        os.makedirs(deps_dir, exist_ok=True)

    if not os.path.isfile(asset_path):
        raise TLSClientException(
            f"TLS binary not found at {asset_path}. "
            f"Place your compiled library named '{asset_name}' in '{deps_dir}/'."
        )

    return asset_name
