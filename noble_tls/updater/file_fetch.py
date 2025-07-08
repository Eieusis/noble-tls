import asyncio
import os
import random
from functools import wraps
from typing import Tuple

from noble_tls.utils.asset import generate_asset_name
from noble_tls.utils.asset import root_dir
from noble_tls.exceptions.exceptions import TLSClientException
import httpx

owner = 'bogdanfinn'
repo = 'tls-client'
url = f'https://api.github.com/repos/{owner}/{repo}/releases/latest'
root_directory = root_dir()
GITHUB_TOKEN = os.getenv("GH_TOKEN")


def auto_retry(retries: int):
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
                    await asyncio.sleep(0.1)

        return wrapper

    return decorator


@auto_retry(retries=3)
async def get_latest_release() -> Tuple[str, list]:
    """
    Fetches the latest release from the GitHub API.

    :return: Latest release tag name, and a list of assets
    """
    # Make a GET request to the GitHub API
    proxies = [
        "http://abelito:poh2raiC3ei4x@87.229.36.2:2500",
        "http://abelito:poh2raiC3ei4x@87.229.36.3:2501",
        "http://abelito:poh2raiC3ei4x@87.229.36.4:2502",
        "http://abelito:poh2raiC3ei4x@87.229.36.5:2503",
        "http://abelito:poh2raiC3ei4x@87.229.36.6:2504",
        "http://abelito:poh2raiC3ei4x@87.229.36.7:2505",
        "http://abelito:poh2raiC3ei4x@87.229.36.8:2506",
        "http://abelito:poh2raiC3ei4x@87.229.36.9:2507",
        "http://abelito:poh2raiC3ei4x@87.229.36.10:2508",
        "http://abelito:poh2raiC3ei4x@87.229.36.11:2509",
        "http://abelito:poh2raiC3ei4x@87.229.36.12:2510",
        "http://abelito:poh2raiC3ei4x@87.229.36.13:2511",
        "http://abelito:poh2raiC3ei4x@87.229.36.14:2512",
        "http://abelito:poh2raiC3ei4x@87.229.36.15:2513",
        "http://abelito:poh2raiC3ei4x@87.229.36.16:2514",
        "http://abelito:poh2raiC3ei4x@87.229.36.17:2515",
        "http://abelito:poh2raiC3ei4x@87.229.36.18:2516",
        "http://abelito:poh2raiC3ei4x@87.229.36.19:2517",
        "http://abelito:poh2raiC3ei4x@87.229.36.20:2518",
        "http://abelito:poh2raiC3ei4x@87.229.36.21:2519",
        "http://abelito:poh2raiC3ei4x@87.229.36.22:2520",
        "http://abelito:poh2raiC3ei4x@87.229.36.23:2521",
        "http://abelito:poh2raiC3ei4x@87.229.36.24:2522",
        "http://abelito:poh2raiC3ei4x@87.229.36.25:2523",
        "http://abelito:poh2raiC3ei4x@87.229.36.26:2524",
        "http://abelito:poh2raiC3ei4x@87.229.36.27:2525",
        "http://abelito:poh2raiC3ei4x@87.229.36.28:2526",
        "http://abelito:poh2raiC3ei4x@87.229.36.29:2527",
        "http://abelito:poh2raiC3ei4x@87.229.36.30:2528",
        "http://abelito:poh2raiC3ei4x@87.229.36.31:2529",
        "http://abelito:poh2raiC3ei4x@87.229.36.32:2530",
        "http://abelito:poh2raiC3ei4x@87.229.36.33:2531",
        "http://abelito:poh2raiC3ei4x@87.229.36.34:2532",
        "http://abelito:poh2raiC3ei4x@87.229.36.35:2533",
        "http://abelito:poh2raiC3ei4x@87.229.36.36:2534",
        "http://abelito:poh2raiC3ei4x@87.229.36.37:2535",
        "http://abelito:poh2raiC3ei4x@87.229.36.38:2536",
        "http://abelito:poh2raiC3ei4x@87.229.36.39:2537",
        "http://abelito:poh2raiC3ei4x@87.229.36.40:2538",
        "http://abelito:poh2raiC3ei4x@87.229.36.41:2539",
        "http://abelito:poh2raiC3ei4x@87.229.36.42:2540",
        "http://abelito:poh2raiC3ei4x@87.229.36.43:2541",
        "http://abelito:poh2raiC3ei4x@87.229.36.44:2542",
        "http://abelito:poh2raiC3ei4x@87.229.36.45:2543",
        "http://abelito:poh2raiC3ei4x@87.229.36.46:2544",
        "http://abelito:poh2raiC3ei4x@87.229.36.47:2545",
        "http://abelito:poh2raiC3ei4x@87.229.36.48:2546",
        "http://abelito:poh2raiC3ei4x@87.229.36.49:2547",
        "http://abelito:poh2raiC3ei4x@87.229.36.50:2548",
        "http://abelito:poh2raiC3ei4x@87.229.36.51:2549",
        "http://abelito:poh2raiC3ei4x@87.229.36.52:2550",
        "http://abelito:poh2raiC3ei4x@87.229.36.53:2551",
        "http://abelito:poh2raiC3ei4x@87.229.36.54:2552",
        "http://abelito:poh2raiC3ei4x@87.229.36.55:2553",
        "http://abelito:poh2raiC3ei4x@87.229.36.56:2554",
        "http://abelito:poh2raiC3ei4x@87.229.36.57:2555",
        "http://abelito:poh2raiC3ei4x@87.229.36.58:2556",
        "http://abelito:poh2raiC3ei4x@87.229.36.59:2557",
        "http://abelito:poh2raiC3ei4x@87.229.36.60:2558",
        "http://abelito:poh2raiC3ei4x@87.229.36.61:2559",
        "http://abelito:poh2raiC3ei4x@87.229.36.62:2560",
        "http://abelito:poh2raiC3ei4x@87.229.36.63:2561",
        "http://abelito:poh2raiC3ei4x@87.229.36.64:2562",
        "http://abelito:poh2raiC3ei4x@87.229.36.65:2563",
        "http://abelito:poh2raiC3ei4x@87.229.36.66:2564",
        "http://abelito:poh2raiC3ei4x@87.229.36.67:2565",
        "http://abelito:poh2raiC3ei4x@87.229.36.68:2566",
        "http://abelito:poh2raiC3ei4x@87.229.36.69:2567",
        "http://abelito:poh2raiC3ei4x@87.229.36.70:2568",
        "http://abelito:poh2raiC3ei4x@87.229.36.71:2569",
        "http://abelito:poh2raiC3ei4x@87.229.36.72:2570",
        "http://abelito:poh2raiC3ei4x@87.229.36.73:2571",
        "http://abelito:poh2raiC3ei4x@87.229.36.74:2572",
        "http://abelito:poh2raiC3ei4x@87.229.36.75:2573",
        "http://abelito:poh2raiC3ei4x@87.229.36.76:2574",
        "http://abelito:poh2raiC3ei4x@87.229.36.77:2575",
        "http://abelito:poh2raiC3ei4x@87.229.36.78:2576",
        "http://abelito:poh2raiC3ei4x@87.229.36.79:2577",
        "http://abelito:poh2raiC3ei4x@87.229.36.80:2578",
        "http://abelito:poh2raiC3ei4x@87.229.36.81:2579",
        "http://abelito:poh2raiC3ei4x@87.229.36.82:2580",
        "http://abelito:poh2raiC3ei4x@87.229.36.83:2581",
        "http://abelito:poh2raiC3ei4x@87.229.36.84:2582",
        "http://abelito:poh2raiC3ei4x@87.229.36.85:2583",
        "http://abelito:poh2raiC3ei4x@87.229.36.86:2584",
        "http://abelito:poh2raiC3ei4x@87.229.36.87:2585",
        "http://abelito:poh2raiC3ei4x@87.229.36.88:2586",
        "http://abelito:poh2raiC3ei4x@87.229.36.89:2587",
        "http://abelito:poh2raiC3ei4x@87.229.36.90:2588",
        "http://abelito:poh2raiC3ei4x@87.229.36.91:2589",
        "http://abelito:poh2raiC3ei4x@87.229.36.92:2590",
        "http://abelito:poh2raiC3ei4x@87.229.36.93:2591",
        "http://abelito:poh2raiC3ei4x@87.229.36.94:2592",
        "http://abelito:poh2raiC3ei4x@87.229.36.95:2593",
        "http://abelito:poh2raiC3ei4x@87.229.36.96:2594",
        "http://abelito:poh2raiC3ei4x@87.229.36.97:2595",
        "http://abelito:poh2raiC3ei4x@87.229.36.98:2596",
        "http://abelito:poh2raiC3ei4x@87.229.36.99:2597",
        "http://abelito:poh2raiC3ei4x@87.229.36.100:2598",
        "http://abelito:poh2raiC3ei4x@87.229.36.101:2599",
        "http://abelito:poh2raiC3ei4x@87.229.36.102:2600",
        "http://abelito:poh2raiC3ei4x@87.229.36.103:2601",
        "http://abelito:poh2raiC3ei4x@87.229.36.104:2602",
        "http://abelito:poh2raiC3ei4x@87.229.36.105:2603",
        "http://abelito:poh2raiC3ei4x@87.229.36.106:2604",
        "http://abelito:poh2raiC3ei4x@87.229.36.107:2605",
        "http://abelito:poh2raiC3ei4x@87.229.36.108:2606",
        "http://abelito:poh2raiC3ei4x@87.229.36.109:2607",
        "http://abelito:poh2raiC3ei4x@87.229.36.110:2608",
        "http://abelito:poh2raiC3ei4x@87.229.36.111:2609",
        "http://abelito:poh2raiC3ei4x@87.229.36.112:2610",
        "http://abelito:poh2raiC3ei4x@87.229.36.113:2611",
        "http://abelito:poh2raiC3ei4x@87.229.36.114:2612",
        "http://abelito:poh2raiC3ei4x@87.229.36.115:2613",
        "http://abelito:poh2raiC3ei4x@87.229.36.116:2614",
        "http://abelito:poh2raiC3ei4x@87.229.36.117:2615",
        "http://abelito:poh2raiC3ei4x@87.229.36.118:2616",
        "http://abelito:poh2raiC3ei4x@87.229.36.119:2617",
        "http://abelito:poh2raiC3ei4x@87.229.36.120:2618",
        "http://abelito:poh2raiC3ei4x@87.229.36.121:2619",
        "http://abelito:poh2raiC3ei4x@87.229.36.122:2620",
        "http://abelito:poh2raiC3ei4x@87.229.36.123:2621",
        "http://abelito:poh2raiC3ei4x@87.229.36.124:2622",
        "http://abelito:poh2raiC3ei4x@87.229.36.125:2623",
        "http://abelito:poh2raiC3ei4x@87.229.36.126:2624",
        "http://abelito:poh2raiC3ei4x@87.229.36.127:2625",
        "http://abelito:poh2raiC3ei4x@87.229.36.128:2626",
        "http://abelito:poh2raiC3ei4x@87.229.36.129:2627",
        "http://abelito:poh2raiC3ei4x@87.229.36.130:2628",
        "http://abelito:poh2raiC3ei4x@87.229.36.131:2629",
        "http://abelito:poh2raiC3ei4x@87.229.36.132:2630",
        "http://abelito:poh2raiC3ei4x@87.229.36.133:2631",
        "http://abelito:poh2raiC3ei4x@87.229.36.134:2632",
        "http://abelito:poh2raiC3ei4x@87.229.36.135:2633",
        "http://abelito:poh2raiC3ei4x@87.229.36.136:2634",
        "http://abelito:poh2raiC3ei4x@87.229.36.137:2635",
        "http://abelito:poh2raiC3ei4x@87.229.36.138:2636",
        "http://abelito:poh2raiC3ei4x@87.229.36.139:2637",
        "http://abelito:poh2raiC3ei4x@87.229.36.140:2638",
        "http://abelito:poh2raiC3ei4x@87.229.36.141:2639",
        "http://abelito:poh2raiC3ei4x@87.229.36.142:2640",
        "http://abelito:poh2raiC3ei4x@87.229.36.143:2641",
        "http://abelito:poh2raiC3ei4x@87.229.36.144:2642",
        "http://abelito:poh2raiC3ei4x@87.229.36.145:2643",
        "http://abelito:poh2raiC3ei4x@87.229.36.146:2644",
        "http://abelito:poh2raiC3ei4x@87.229.36.147:2645",
        "http://abelito:poh2raiC3ei4x@87.229.36.148:2646",
        "http://abelito:poh2raiC3ei4x@87.229.36.149:2647",
        "http://abelito:poh2raiC3ei4x@87.229.36.150:2648",
        "http://abelito:poh2raiC3ei4x@87.229.36.151:2649",
        "http://abelito:poh2raiC3ei4x@87.229.36.152:2650",
        "http://abelito:poh2raiC3ei4x@87.229.36.153:2651",
        "http://abelito:poh2raiC3ei4x@87.229.36.154:2652",
        "http://abelito:poh2raiC3ei4x@87.229.36.155:2653",
        "http://abelito:poh2raiC3ei4x@87.229.36.156:2654",
        "http://abelito:poh2raiC3ei4x@87.229.36.157:2655",
        "http://abelito:poh2raiC3ei4x@87.229.36.158:2656",
        "http://abelito:poh2raiC3ei4x@87.229.36.159:2657",
        "http://abelito:poh2raiC3ei4x@87.229.36.160:2658",
        "http://abelito:poh2raiC3ei4x@87.229.36.161:2659",
        "http://abelito:poh2raiC3ei4x@87.229.36.162:2660",
        "http://abelito:poh2raiC3ei4x@87.229.36.163:2661",
        "http://abelito:poh2raiC3ei4x@87.229.36.164:2662",
        "http://abelito:poh2raiC3ei4x@87.229.36.165:2663",
        "http://abelito:poh2raiC3ei4x@87.229.36.166:2664",
        "http://abelito:poh2raiC3ei4x@87.229.36.167:2665",
        "http://abelito:poh2raiC3ei4x@87.229.36.168:2666",
        "http://abelito:poh2raiC3ei4x@87.229.36.169:2667",
        "http://abelito:poh2raiC3ei4x@87.229.36.170:2668",
        "http://abelito:poh2raiC3ei4x@87.229.36.171:2669",
        "http://abelito:poh2raiC3ei4x@87.229.36.172:2670",
        "http://abelito:poh2raiC3ei4x@87.229.36.173:2671",
        "http://abelito:poh2raiC3ei4x@87.229.36.174:2672",
        "http://abelito:poh2raiC3ei4x@87.229.36.175:2673",
        "http://abelito:poh2raiC3ei4x@87.229.36.176:2674",
        "http://abelito:poh2raiC3ei4x@87.229.36.177:2675",
        "http://abelito:poh2raiC3ei4x@87.229.36.178:2676",
        "http://abelito:poh2raiC3ei4x@87.229.36.179:2677",
        "http://abelito:poh2raiC3ei4x@87.229.36.180:2678",
        "http://abelito:poh2raiC3ei4x@87.229.36.181:2679",
        "http://abelito:poh2raiC3ei4x@87.229.36.182:2680",
        "http://abelito:poh2raiC3ei4x@87.229.36.183:2681",
        "http://abelito:poh2raiC3ei4x@87.229.36.184:2682",
        "http://abelito:poh2raiC3ei4x@87.229.36.185:2683",
        "http://abelito:poh2raiC3ei4x@87.229.36.186:2684",
        "http://abelito:poh2raiC3ei4x@87.229.36.187:2685",
        "http://abelito:poh2raiC3ei4x@87.229.36.188:2686",
        "http://abelito:poh2raiC3ei4x@87.229.36.189:2687",
        "http://abelito:poh2raiC3ei4x@87.229.36.190:2688",
        "http://abelito:poh2raiC3ei4x@87.229.36.191:2689",
        "http://abelito:poh2raiC3ei4x@87.229.36.192:2690",
        "http://abelito:poh2raiC3ei4x@87.229.36.193:2691",
        "http://abelito:poh2raiC3ei4x@87.229.36.194:2692",
        "http://abelito:poh2raiC3ei4x@87.229.36.195:2693",
        "http://abelito:poh2raiC3ei4x@87.229.36.196:2694",
        "http://abelito:poh2raiC3ei4x@87.229.36.197:2695",
        "http://abelito:poh2raiC3ei4x@87.229.36.198:2696",
        "http://abelito:poh2raiC3ei4x@87.229.36.199:2697",
        "http://abelito:poh2raiC3ei4x@87.229.36.200:2698",
        "http://abelito:poh2raiC3ei4x@87.229.36.201:2699",
        "http://abelito:poh2raiC3ei4x@87.229.36.202:2700",
        "http://abelito:poh2raiC3ei4x@87.229.36.203:2701",
        "http://abelito:poh2raiC3ei4x@87.229.36.204:2702",
        "http://abelito:poh2raiC3ei4x@87.229.36.205:2703",
        "http://abelito:poh2raiC3ei4x@87.229.36.206:2704",
        "http://abelito:poh2raiC3ei4x@87.229.36.207:2705",
        "http://abelito:poh2raiC3ei4x@87.229.36.208:2706",
        "http://abelito:poh2raiC3ei4x@87.229.36.209:2707",
        "http://abelito:poh2raiC3ei4x@87.229.36.210:2708",
        "http://abelito:poh2raiC3ei4x@87.229.36.211:2709",
        "http://abelito:poh2raiC3ei4x@87.229.36.212:2710",
        "http://abelito:poh2raiC3ei4x@87.229.36.213:2711",
        "http://abelito:poh2raiC3ei4x@87.229.36.214:2712",
        "http://abelito:poh2raiC3ei4x@87.229.36.215:2713",
        "http://abelito:poh2raiC3ei4x@87.229.36.216:2714",
        "http://abelito:poh2raiC3ei4x@87.229.36.217:2715",
        "http://abelito:poh2raiC3ei4x@87.229.36.218:2716",
        "http://abelito:poh2raiC3ei4x@87.229.36.219:2717",
        "http://abelito:poh2raiC3ei4x@87.229.36.220:2718",
        "http://abelito:poh2raiC3ei4x@87.229.36.221:2719",
        "http://abelito:poh2raiC3ei4x@87.229.36.222:2720",
        "http://abelito:poh2raiC3ei4x@87.229.36.223:2721",
        "http://abelito:poh2raiC3ei4x@87.229.36.224:2722",
        "http://abelito:poh2raiC3ei4x@87.229.36.225:2723",
        "http://abelito:poh2raiC3ei4x@87.229.36.226:2724",
        "http://abelito:poh2raiC3ei4x@87.229.36.227:2725",
        "http://abelito:poh2raiC3ei4x@87.229.36.228:2726",
        "http://abelito:poh2raiC3ei4x@87.229.36.229:2727",
        "http://abelito:poh2raiC3ei4x@87.229.36.230:2728",
        "http://abelito:poh2raiC3ei4x@87.229.36.231:2729",
        "http://abelito:poh2raiC3ei4x@87.229.36.232:2730",
        "http://abelito:poh2raiC3ei4x@87.229.36.233:2731",
        "http://abelito:poh2raiC3ei4x@87.229.36.234:2732",
        "http://abelito:poh2raiC3ei4x@87.229.36.235:2733",
        "http://abelito:poh2raiC3ei4x@87.229.36.236:2734",
        "http://abelito:poh2raiC3ei4x@87.229.36.237:2735",
        "http://abelito:poh2raiC3ei4x@87.229.36.238:2736",
        "http://abelito:poh2raiC3ei4x@87.229.36.239:2737",
        "http://abelito:poh2raiC3ei4x@87.229.36.240:2738",
        "http://abelito:poh2raiC3ei4x@87.229.36.241:2739",
        "http://abelito:poh2raiC3ei4x@87.229.36.242:2740",
        "http://abelito:poh2raiC3ei4x@87.229.36.243:2741",
        "http://abelito:poh2raiC3ei4x@87.229.36.244:2742",
        "http://abelito:poh2raiC3ei4x@87.229.36.245:2743",
        "http://abelito:poh2raiC3ei4x@87.229.36.246:2744",
        "http://abelito:poh2raiC3ei4x@87.229.36.247:2745",
        "http://abelito:poh2raiC3ei4x@87.229.36.248:2746",
        "http://abelito:poh2raiC3ei4x@87.229.36.249:2747",
        "http://abelito:poh2raiC3ei4x@87.229.36.250:2748",
        "http://abelito:poh2raiC3ei4x@87.229.36.251:2749",
        "http://abelito:poh2raiC3ei4x@87.229.36.252:2750",
        "http://abelito:poh2raiC3ei4x@87.229.36.253:2751",
        "http://abelito:poh2raiC3ei4x@87.229.36.254:2752"
    ]
    
    proxy = random.choice(proxies)
    async with httpx.AsyncClient(proxy=proxy) as client:
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'noble-tls'
        }
        response = await client.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()  # Parse the JSON data from the response
        version_num = data['tag_name'].replace('v', '')  # Return the tag name without the 'v' prefix
        if 'assets' not in data:
            raise TLSClientException(f"Version {version_num} does not have any assets.")

        # Get assets
        assets = data['assets']
        return version_num, assets
    else:
        raise TLSClientException(f"Failed to fetch the latest release. Status code: {response.status_code}")


async def download_and_save_asset(
        asset_url: str,
        asset_name: str,
        version: str
) -> None:
    # Download
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

    asset_name = generate_asset_name(custom_part=repo, version=version_num)
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
