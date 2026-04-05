#region Libaries
import os, requests
from colorama import init, Fore, Style
import data
#endregion

init(autoreset = True)

#region Version
GITHUB_API = "https://api.github.com/repos/yehan-mov/school-bag-manager/releases/latest"
CURRENT_VERSION = "1.1.0"
#endregion

#region Functions
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def check_for_update():
    try:
        response = requests.get(GITHUB_API, timeout = 5)
        data = response.json()

        latest_version = data.get("tag_name", "")

        if latest_version and latest_version != CURRENT_VERSION:
            return latest_version
    except:
        pass
    return None
#endregion