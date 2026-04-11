import data, utils, usermenu
from colorama import init, Fore, Style

init(autoreset = True)

def main_menu():
    global data
    app_data = data.load_data()

    utils.update_status()
    utils.clear()

    while True:
        print(f"\n{utils.AMBER}--- School Bag Management ---{Style.RESET_ALL}")
        print("[1] Select user")
        print("[2] Settings")
        print("[0] Exit")

        try:
            choice = int(input(f"{Fore.CYAN}> {Style.RESET_ALL}"))
        except ValueError:
            print(f"{Fore.RED}ERR: Numbers only{Style.RESET_ALL}")
            continue

        if choice == 0:
            confirm = input(f"Exit? (Y/N){Fore.CYAN} > {Style.RESET_ALL}").upper().strip()
            if confirm == "Y":
                break

        elif choice == 2:
            usermenu.settings(app_data)

        elif choice == 1:
            if not app_data["users"]:
                print(f"{Fore.YELLOW}No users found{Style.RESET_ALL}")
                continue

            users = list(app_data["users"].keys())
            print("\nUsers:")
            for i, u in enumerate(users, 1):
                print(f"[{i}] {u}")

            try:
                u_choice = int(input(f"{Fore.CYAN}> {Style.RESET_ALL}"))
                username = users[u_choice - 1]
            except:
                print(f"{Fore.RED}ERR: Invalid selection{Style.RESET_ALL}")
                continue

            usermenu.user_menu(username, app_data, app_data["users"][username])

        else:
            print(f"{Fore.RED}ERR: Invalid option selected. Please try again.{Style.RESET_ALL}")
            continue

if __name__ == "__main__":
    main_menu()