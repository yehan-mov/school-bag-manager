import utils, data
from colorama import init, Fore, Style

init(autoreset = True)

def settings(app_data):
    utils.clear()

    while True:
        print(f"{Fore.YELLOW}{Style.BRIGHT}--- Settings ---{Style.RESET_ALL}")
        print("[1] Add user")
        print("[2] About")
        print("[0] Back")

        try:
            choice = int(input(f"{Fore.CYAN}> {Style.RESET_ALL}"))
        except ValueError:
            print(f"{Fore.RED}ERR: Numbers only{Style.RESET_ALL}")
            continue

        if choice == 0:
            return
        
        elif choice == 1:
            data.add_user(app_data)

        elif choice == 2:
            print(f"School Bag Manager {utils.CURRENT_VERSION}")
            print("Never forget a textbook again — manage your school bag from the terminal.")

            print("\nMade by Yehan Mullick")
            print("Made on Python 3.13")
            print("IDK what to write here tbh.")
        
        else:
            print(f"{Fore.RED}{Style.BRIGHT}ERR: Invalid option{Style.RESET_ALL}")