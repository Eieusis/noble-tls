import asyncio
import os
import random
from functools import wraps
from typing import Tuple

from noble_tls.utils.asset import generate_asset_name
from noble_tls.utils.asset import root_dir
from noble_tls.exceptions.exceptions import TLSClientException
import httpx


owner = 'yeet-robotics'
repo = 'tls-client-fixed'
asset_prefix = 'tls-client'
url = f'https://api.github.com/repos/{owner}/{repo}/releases/latest'

root_directory = root_dir()
GITHUB_TOKEN = os.getenv("GH_TOKEN")


def auto_retry(retries: int, base_delay: float = 1.0):
    """
    Retry decorator with exponential backoff.
    On 429 responses, waits longer based on retry count.

    :param retries: Maximum number of retry attempts
    :param base_delay: Initial delay in seconds (doubles each retry)
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            attempt = 0
            while attempt <= retries:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt > retries:
                        print(f">> Failed after {attempt} attempts with error: {e}")
                        raise e
                    delay = base_delay * (2 ** (attempt - 1))
                    print(f">> Attempt {attempt}/{retries} failed: {e}. Retrying in {delay:.1f}s...")
                    await asyncio.sleep(delay)

        return wrapper

    return decorator


@auto_retry(retries=5, base_delay=2.0)
async def get_latest_release() -> Tuple[str, list]:
    """
    Fetches the latest release from the GitHub API.
    Tries multiple proxies with fallback to direct connection.

    :return: Latest release tag name, and a list of assets
    """
    proxies = [
        "http://wftdtauq-1:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-2:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-3:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-4:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-5:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-6:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-7:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-8:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-9:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-10:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-11:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-12:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-13:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-14:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-15:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-16:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-17:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-18:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-19:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-20:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-21:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-22:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-23:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-24:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-25:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-26:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-27:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-28:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-29:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-30:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-31:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-32:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-33:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-34:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-35:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-36:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-37:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-38:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-39:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-40:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-41:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-42:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-43:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-44:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-45:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-46:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-47:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-48:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-49:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-50:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-51:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-52:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-53:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-54:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-55:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-56:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-57:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-58:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-59:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-60:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-61:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-62:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-63:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-64:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-65:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-66:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-67:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-68:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-69:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-70:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-71:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-72:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-73:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-74:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-75:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-76:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-77:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-78:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-79:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-80:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-81:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-82:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-83:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-84:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-85:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-86:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-87:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-88:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-89:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-90:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-91:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-92:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-93:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-94:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-95:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-96:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-97:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-98:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-99:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-100:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-101:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-102:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-103:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-104:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-105:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-106:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-107:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-108:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-109:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-110:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-111:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-112:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-113:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-114:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-115:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-116:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-117:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-118:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-119:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-120:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-121:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-122:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-123:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-124:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-125:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-126:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-127:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-128:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-129:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-130:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-131:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-132:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-133:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-134:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-135:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-136:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-137:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-138:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-139:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-140:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-141:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-142:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-143:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-144:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-145:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-146:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-147:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-148:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-149:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-150:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-151:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-152:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-153:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-154:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-155:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-156:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-157:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-158:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-159:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-160:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-161:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-162:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-163:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-164:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-165:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-166:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-167:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-168:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-169:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-170:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-171:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-172:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-173:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-174:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-175:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-176:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-177:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-178:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-179:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-180:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-181:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-182:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-183:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-184:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-185:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-186:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-187:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-188:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-189:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-190:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-191:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-192:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-193:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-194:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-195:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-196:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-197:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-198:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-199:lc694ck8rnos@p.webshare.io:80",
        "http://wftdtauq-200:lc694ck8rnos@p.webshare.io:80",
    ]
    
    random.shuffle(proxies)
    chosen_proxies = proxies[:5] + [None]
    last_status_code = None

    for proxy in chosen_proxies:
        try:
            async with httpx.AsyncClient(proxy=proxy, timeout=15.0) as client:
                headers = {
                    'Accept': 'application/vnd.github.v3+json',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
                }
                if GITHUB_TOKEN:
                    headers['Authorization'] = f'token {GITHUB_TOKEN}'

                response = await client.get(url, headers=headers)
                last_status_code = response.status_code

                if response.status_code == 200:
                    data = response.json()
                    version_num = data['tag_name'].replace('v', '')
                    if 'assets' not in data:
                        raise TLSClientException(f"Version {version_num} does not have any assets.")

                    assets = data['assets']
                    print(f">> Latest version: {version_num}")
                    return version_num, assets

                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 5))
                    proxy_label = proxy or "direct"
                    print(f">> Rate limited (429) via {proxy_label}, waiting {retry_after}s before next proxy...")
                    await asyncio.sleep(retry_after)
                    continue

                print(f">> Got status {response.status_code} via {proxy or 'direct'}, trying next proxy...")

        except TLSClientException:
            raise
        except Exception as e:
            print(f">> Proxy {proxy or 'direct'} failed ({e}), trying another proxy...")

    raise TLSClientException(f"Failed to fetch the latest release. Status code: {last_status_code}")


async def download_and_save_asset(
        asset_url: str,
        asset_name: str,
        version: str
) -> None:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        headers = {
            'Accept': 'application/octet-stream',
            'User-Agent': 'rawandahmad698',
            'Connection': 'keep-alive'
        }
        if GITHUB_TOKEN:
            headers["Authorization"] = f"token {GITHUB_TOKEN}"
            print(">> Using GitHub token for authentication.")

        response = await client.get(asset_url, headers=headers)
        if response.status_code != 200:
            raise TLSClientException(f"Failed to download asset {asset_name}. Status code: {response.status_code}")

        with open(f'{root_directory}/dependencies/{asset_name}', 'wb') as f:
            f.write(response.content)

        # Save version info
        await save_version_info(asset_name, version)


async def save_version_info(asset_name: str, version: str):
    """
    Save version info to a hidden .version file in root_dir/dependencies
    """
    with open(f'{root_directory}/dependencies/.version', 'w') as f:
        f.write(f"{asset_name} {version}")


def delete_version_info():
    """
    Delete everything inside dependencies/.version
    """
    try:
        # Delete all files in dependencies
        for file in os.listdir(f'{root_directory}/dependencies'):
            os.remove(f'{root_directory}/dependencies/{file}')
    except FileNotFoundError:
        pass


def read_version_info():
    """
    Read version info from a hidden .version file in root_dir/dependencies
    """
    try:
        with open(f'{root_directory}/dependencies/.version', 'r') as f:
            data = f.read()
            data = data.split(' ')
            return data[0], data[1]
    except FileNotFoundError:
        return None, None


async def download_if_necessary():
    version_num, asset_url = await get_latest_release()
    if not asset_url or not version_num:
        raise TLSClientException(f"Version {version_num} does not have any assets.")

    asset_name = generate_asset_name(custom_part=asset_prefix, version=version_num)
    # Check if asset name is in the list of assets in root dir/dependencies
    if os.path.exists(f'{root_directory}/dependencies/{asset_name}'):
        return

    download_url = [asset['browser_download_url'] for asset in asset_url if asset['name'] == asset_name]
    if len(download_url) == 0:
        raise TLSClientException(f"Unable to find asset {asset_name} for version {version_num}.")

    download_url = download_url[0]
    await download_and_save_asset(download_url, asset_name, version_num)


async def update_if_necessary():
    current_asset, current_version = read_version_info()
    if not current_asset or not current_version:
        raise TLSClientException("Unable to read version info, no TLS libs found, use download_if_necessary()")

    version_num, asset_url = await get_latest_release()
    if not asset_url or not version_num:
        raise TLSClientException(f"Version {version_num} does not have any assets.")

    if version_num != current_version:
        print(f">> Current version {current_version} is outdated, downloading the latest TLS release...")
        await download_if_necessary()


if __name__ == "__main__":
    asyncio.run(update_if_necessary())
