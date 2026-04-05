from colorama import init, Fore, Style
import sys
import utils, core, data

init(autoreset=True)

def subject_menu(app_data, user_data):
    utils.clear()

    while True:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}--- Subject Menu ---{Style.RESET_ALL}")
        print("[1] Show all subjects")
        print("[2] Add subject")
        print("[3] Remove subject")
        print("[4] Back")
        print("[0] Return back to Main Menu")

        try:
            choice = int(input(f"{Fore.CYAN}> {Style.RESET_ALL}"))
        except ValueError:
            print(f"{Fore.RED}ERR: Numbers only{Style.RESET_ALL}")
            continue

        if choice == 0:
            return
        
        if choice == 4:
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
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}--- Timetable Menu ---{Style.RESET_ALL}")
        print("[1] Add to timetable")
        print("[2] View timetable")
        print("[3] Remove from timetable")
        print("[4] Back")
        print("[0] Complete Exit")

        try:
            choice = int(input(f"{Fore.CYAN}> {Style.RESET_ALL}"))
        except ValueError:
            print(f"{Fore.RED}ERR: Numbers only{Style.RESET_ALL}")
            continue

        if choice == 0:
            sys.exit()
        
        if choice == 4:
            return
        
        elif choice == 1:
            data.add_to_timetable(app_data, user_data)

        elif choice == 2:
            data.veiw_timetable(user_data)

        elif choice == 3:
            data.remove_from_timetable(app_data, user_data)

        else:
            print(f"{Fore.RED}ERR: Invalid option{Style.RESET_ALL}")

def user_menu(username, app_data, user_data):
    utils.clear()

    while True:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}--- Hello {username}! ---{Style.RESET_ALL}")
        print("[1] Show today's plan")
        print("[2] Show tomorrow's plan")
        print("[3] Subject options >>>")
        print("[4] Timetable options >>>")
        print("[5] Back")
        print("[0] Complete Exit")

        try:
            choice = int(input(f"{Fore.CYAN}> {Style.RESET_ALL}"))
        except ValueError:
            print(f"{Fore.RED}ERR: Numbers only{Style.RESET_ALL}")
            continue

        if choice == 0:
            sys.exit()

        if choice == 5:
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