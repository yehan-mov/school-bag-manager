from colorama import init, Fore, Style
import utils, core, data

init(autoreset=True)

def settings(app_data):
    utils.clear()

    while True:
        print(f"{utils.AMBER}--- Settings ---{Style.RESET_ALL}")
        print("[0] Return...")

        print(f"\n{utils.AMBER}--- Options ---{Style.RESET_ALL}")
        print("[1] Add user")
        print("[2] About")
        print(f"{Fore.RED}[3] A Complete Clean up{Style.RESET_ALL}")

        try:
            choice = int(input(f"{Fore.CYAN}> {Style.RESET_ALL}"))
        except ValueError:
            print(f"{Fore.RED}ERR: This field accepts numbers only.{Style.RESET_ALL}")
            continue

        if choice == 0:
            return
        
        elif choice == 1:
            data.add_user(app_data)

        elif choice == 2:
            print(f"School Bag Manager v{utils.CURRENT_VERSION}")
            print("Never forget a textbook again - manage your school bag from the terminal.")

            print("\n Made by Yehan Mullick")
            print("Made on Python 3.13")
            print("If you are seeeing this then THANK YOU for using this")

        elif choice == 3:
            print(f"{Fore.YELLOW}!! Warning !!{Style.RESET_ALL}")
            print("This will delete all your subjects from the database")
            print("This operation is not reversiable.")
            print("\nDo you wish to proceed? (Y/N)")

            user_option = input(f"{Fore.CYAN}> {Style.RESET_ALL}").strip().upper()

            if user_option != "Y":
                print("Operation Cancelled")
            
            else:
                print("This is still in progress")

        else:
            print(f"{Fore.RED}ERR: Invalid option! Please try again.{Style.RESET_ALL}")
            continue

def subject_menu(app_data, user_data):
    utils.clear()

    while True:
        print(f"\n{utils.AMBER}--- Subject Menu ---{Style.RESET_ALL}")
        print("[0] Back...")

        print(f"\n{utils.AMBER}--- Options ---{Style.RESET_ALL}")
        print("[1] Show all subjects")
        print("[2] Add subject")
        print("[3] Remove subject")

        try:
            choice = int(input(f"{Fore.CYAN}> {Style.RESET_ALL}"))
        except ValueError:
            print(f"{Fore.RED}ERR: Numbers only{Style.RESET_ALL}")
            continue

        if choice == 0:
            return

        elif choice == 1:
            data.show_all_subject(app_data, user_data)

        elif choice == 2:
            data.add_subject(app_data, user_data)

        elif choice == 3:
            data.remove_subject(app_data, user_data)

        else:
            print(f"{Fore.RED}ERR: Invalid option{Style.RESET_ALL}")

def timetable_menu(app_data, user_data):
    utils.clear()

    while True:
        print(f"\n{utils.AMBER}--- Timetable Menu ---{Style.RESET_ALL}")
        print("[0] Back...")

        print(f"\n{utils.AMBER}--- Options ---{Style.RESET_ALL}")
        print("[1] Add to timetable")
        print("[2] View timetable")
        print("[3] Remove subject")

        try:
            choice = int(input(f"{Fore.CYAN}> {Style.RESET_ALL}"))
        except ValueError:
            print(f"{Fore.RED}ERR: Numbers only{Style.RESET_ALL}")
            continue

        if choice == 0:
            return
        
        elif choice == 1:
            data.add_to_timetable(app_data, user_data)

        elif choice == 2:
            data.view_timetable(user_data)

        elif choice == 3:
            data.remove_from_timetable(app_data, user_data)

        else:
            print(f"{Fore.RED}ERR: Invalid option{Style.RESET_ALL}")

def user_menu(username, app_data, user_data):
    utils.clear()

    while True:
        print(f"\n{utils.AMBER}--- Hello {username}! ---{Style.RESET_ALL}")
        print("--- Menu ---")
        print("[0] Return")

        print(f"\n{utils.AMBER}--- Plans ---{Style.RESET_ALL}")
        print("[1] Show today's plan")
        print("[2] Show tomorrow's plan")

        print(f"\n{utils.AMBER}--- Options ---{Style.RESET_ALL}")
        print("[3] Subject options >>>")
        print("[4] Timetable options >>>")

        try:
            choice = int(input(f"{Fore.CYAN}> {Style.RESET_ALL}"))
        except ValueError:
            print(f"{Fore.RED}ERR: Numbers only{Style.RESET_ALL}")
            continue

        if choice == 0:
            return
        
        elif choice == 1:
            core.show_today_plan(app_data, user_data)

        elif choice == 2:
            core.show_tomorrow_plan(app_data, user_data)

        elif choice == 3:
            subject_menu(app_data, user_data)

        elif choice == 4:
            timetable_menu(app_data, user_data)

        else:
            print(f"{Fore.RED}ERR: Invalid option{Style.RESET_ALL}")