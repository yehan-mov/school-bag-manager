import os, requests
from colorama import Fore, Style, init

init(autoreset = True)

GITHUB_API = "https://api.github.com/repos/yehan-mov/school-bag-manager/releases/latest"
CURRENT_VERSION = "1.2.0"

AMBER = Fore.YELLOW + Style.BRIGHT

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def version_to_tuple(v):
    return tuple(map(int, v.split(".")))

def check_for_update():
    try:
        respone = requests.get(GITHUB_API, timeout = 5)
        data = respone.json()

        latest_version = data.get("tag_name", "").lstrip("v")

        if not latest_version:
            return None
        
        current_v = version_to_tuple(CURRENT_VERSION)
        latest_v = version_to_tuple(latest_version)

        if current_v < latest_v:
            return ("update", latest_version)
        
        elif current_v > latest_v:
            return ("beta", latest_version)
        
        else:
            return ("latest", latest_version)
        
    except:
        return None
    
def update_status():
    update_info = check_for_update()

    if update_info:
        status, version = update_info

        if status == "update":
            print(f"{Fore.YELLOW}Update available!: {version}{Style.RESET_ALL}")
        
        else:
            None