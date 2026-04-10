import json, sys, os, difflib
from colorama import init, Fore, Style
from datetime import datetime, timedelta

init(autoreset = True)

def get_db_path():
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), "database.json")
    else:
        return "database.json"
    
DB_FILE = get_db_path()

today = datetime.now()
today_name = today.strftime("%A")

tomorrow = today + timedelta(days=1)
tomorrow_name = tomorrow.strftime("%A")

MAX_PERIODS = 8

DAY_MAP = {
    "mon": "Monday", "monday": "Monday",
    "tue": "Tuesday", "tuesday": "Tuesday",
    "wed": "Wednesday", "wednesday": "Wednesday",
    "thu": "Thursday", "thursday": "Thursday",
    "fri": "Friday", "friday": "Friday" 
}

def load_data():
    default_data = {"users": {}}
    
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()

            if not content:
                print(f"{Fore.YELLOW}{Style.DIM}Database empty. Initializing...{Style.RESET_ALL}")
                save_data(default_data)
                return default_data
            
            return json.loads(content)
        
    except FileNotFoundError:
        print(f"{Fore.YELLOW}{Style.DIM}Database not found. Creating new one...{Style.RESET_ALL}")
        save_data(default_data)
        return default_data
    
    except json.JSONDecodeError:
        print(f"{Fore.RED}{Style.BRIGHT}Database corrupted. Resetting...{Style.RESET_ALL}")
        save_data(default_data)
        return default_data
    
def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent = 4)

def add_user(data):
    while True:
        username = input(f"Enter new username{Fore.CYAN} > {Style.RESET_ALL}").strip()

        if username == "0":
            return

        if not username:
            print(f"{Fore.RED}ERR: Username cannot be empty.{Style.RESET_ALL}")
            continue
        
        if not (3 <= len(username) <= 15):
            print(f"{Fore.RED}ERR: Username must be between 3 and 15 characters.{Style.RESET_ALL}")
            continue
        
        if not username.isalnum():
            print(f"{Fore.RED}ERR: Username can only contain letter and numbers (no spaces/symbols).{Style.RESET_ALL}")
            continue

        if username in data["users"]:
            print(f"{Fore.RED}{Style.BRIGHT}ERR: User already exists{Style.RESET_ALL}")
            continue
        
        data["users"][username] = {
            "timetable": {
                "Monday": [],
                "Tuesday": [],
                "Wednesday": [],
                "Thursday": [],
                "Friday": []
            },
            "books": {},
            "bag": []
        }

        save_data(data)
        print("User added successfully!")

        print("\nWould you like to add more users? (Y/N):")
        more = input(f"{Fore.CYAN}> {Style.RESET_ALL}").upper().strip()

        if more != "Y":
            break

def add_subject(data, user_data):
    while True:
        subject = input(f"Enter subject name{Fore.CYAN} > {Style.RESET_ALL}").strip()

        if subject == "0":
            return

        if not subject:
            print(f"{Fore.RED}{Style.BRIGHT}ERR: Subject name cannot be empty{Style.RESET_ALL}")
            continue
        
        if not any(char.isalpha() for char in subject):
            print(f"{Fore.RED}ERR: Please enter a valid subject name. (must contain letters).{Style.RESET_ALL}")
            continue
        
        if subject in user_data["books"]:
            print(f"{Fore.RED}ERR: Subject already exists{Style.RESET_ALL}")
            continue
        
        user_data["books"][subject] = {
            "textbook": f"{subject} Textbook",
            "notebook": f"{subject} Notebook"
        }

        save_data(data)
        print(f"{Fore.GREEN}Subject '{subject}' added!{Style.RESET_ALL}")

        print("\nWould you like to add more subjects? (Y/N)")
        more = input(f"{Fore.CYAN}> {Style.RESET_ALL}").upper().strip()

        if more != "Y":
            break

def show_all_subject(data, user_data):
    if not user_data["books"]:
        print(f"{Fore.YELLOW}No subjects found.{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Subjects:{Style.RESET_ALL}")
    for i, subject in enumerate(user_data["books"], start = 1):
        print(f"{Fore.GREEN}{i}. {subject}{Style.RESET_ALL}")

def remove_subject(data, user_data):
    while True:
        print("Enter subject to remove or type 0 to cancel")
        subject = input(f"{Fore.CYAN}> {Style.RESET_ALL}").strip()

        if subject == "0":
            return

        if subject not in user_data["books"]:
            subjects = list(user_data["books"].keys())

            matches = difflib.get_close_matches(subject, subjects, n = 1, cutoff = 0.6)

            if matches:
                suggestion = matches[0]
                print(f"{Fore.YELLOW}Did you mean '{suggestion}'? (Y/N){Style.RESET_ALL}")
                choice = input(f"{Fore.CYAN}> {Style.RESET_ALL}").strip().upper()

                if choice == "Y":
                    subject = suggestion
                else:
                    continue

            else:
                print(f"{Fore.RED}ERR: Subject not found{Style.RESET_ALL}")
                continue
        
        del user_data["books"][subject]

        for day in user_data["timetable"]:
            user_data["timetable"][day] = [
                sub for sub in user_data["timetable"][day] if sub != subject
            ]

        save_data(data)
        print(f"{Fore.GREEN}Subject '{subject}' removed successfully!{Style.RESET_ALL}")

        print("Would you like to remove more? (Y/N):")
        more = input(f"{Fore.CYAN}> {Style.RESET_ALL}").upper().strip()

        if more != "Y":
            break

def add_to_timetable(data, user_data):
    while True:
        print("Enter day (Monday - Friday) or type 0 to cancel")
        raw_day = input(f"{Fore.CYAN} > {Style.RESET_ALL}").strip().lower()

        if raw_day == "0":
            return

        if raw_day not in DAY_MAP:
            print(f"{Fore.RED}ERR: Invalid day{Style.RESET_ALL}")
            continue

        day = DAY_MAP[raw_day]

        if isinstance(user_data["timetable"][day], list):
            print(f"{Fore.YELLOW}Warning: Converting old timetable format to new format.{Style.RESET_ALL}")
            user_data["timetable"][day] = {}

        day_data = user_data["timetable"][day]

        if len(day_data) > MAX_PERIODS:
            print(f"{Fore.RED}ERR: Maximum {MAX_PERIODS} periods reached for {day}{Style.RESET_ALL}")
            continue

        free_periods = [i for i in range(1, MAX_PERIODS + 1) if i not in day_data]

        print(f"{Fore.YELLOW}Available periods: {', '.join(map(str, free_periods))}{Style.RESET_ALL}")
        
        try:
            period = int(input(f"Enter period number (e.g. 1, 2, 3...){Fore.CYAN} > {Style.RESET_ALL}"))
        except ValueError:
            print(f"{Fore.RED}ERR: Period should be a number{Style.RESET_ALL}")
            continue

        if period not in range(1, MAX_PERIODS + 1):
            print(f"{Fore.RED}ERR: Invalid period (1-{MAX_PERIODS}){Style.RESET_ALL}")
            continue

        subject = input(f"Enter subject to add {Fore.CYAN}> {Style.RESET_ALL}").strip()

        if subject not in user_data["books"]:
            subjects = list(user_data["books"].keys())

            matches = difflib.get_close_matches(subject, subjects, n = 1, cutoff = 0.6)

            if matches:
                suggestion = matches[0]
                print(f"{Fore.YELLOW}Did you mean '{suggestion}'? (Y/N){Style.RESET_ALL}")
                choice = input(f"{Fore.CYAN}> {Style.RESET_ALL}").strip().upper()

                if choice == "Y":
                    subject = suggestion
                else:
                    continue

            else:
                print(f"{Fore.RED}{Style.BRIGHT}ERR: Subject not found in books{Style.RESET_ALL}")
                continue

        if period in day_data:
            print(f"{Fore.YELLOW}Warning: Overwriting existing subject!{Style.RESET_ALL}")

            confirm = input(f"Overwrite? (Y/N){Fore.CYAN} > {Style.RESET_ALL}").upper().strip()

            if confirm != "Y":
                print(f"{Fore.GREEN}Operation cancelled.{Style.RESET_ALL}")
                return

        day_data[period] = subject
        save_data(data)

        print(f"{Fore.GREEN}Added {subject} to {day}, Period {period}!{Style.RESET_ALL}")
        more = input(f"Would you like to add more? (Y/N){Fore.CYAN} > {Style.RESET_ALL}").upper().strip()
        
        if more != "Y":
            break

def view_timetable(user_data):
    print("\n" + "=" * 50)
    print("        Weekly Timetable")
    print("=" * 50)

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    for day in days:
        print(f"\n{day}:")
        print("-" * 30)

        day_data = user_data["timetable"].get(day, {})

        if not day_data:
            print("  No periods assigned.")
            continue

        for period in sorted(day_data, key = int):
            subject = day_data[period]
            print(f"  Period {period}: {subject}")

def remove_from_timetable(data, user_data):
    while True:
        print("Enter day (Monday - Friday) or type 0 to cancel")
        raw_day = input(f"{Fore.CYAN} > {Style.RESET_ALL}").strip().lower()

        if raw_day == "0":
            return

        if raw_day not in DAY_MAP:
            print(f"{Fore.RED}ERR: Invalid day{Style.RESET_ALL}")
            continue

        day = DAY_MAP[raw_day]

        day_data = user_data["timetable"][day]

        if not day_data:
            print(f"{Fore.RED}ERR: No subjects scheduled for {day}.{Style.RESET_ALL}")
            continue

        print(f"{Fore.YELLOW}Current periods for {day}:{Style.RESET_ALL}")
        for period, subject in sorted(day_data.items()):
            print(f"  Period {period}: {subject}")

        try:
            period = int(input(f"Enter period to remove{Fore.CYAN} > {Style.RESET_ALL}"))
        except ValueError:
            print(f"{Fore.RED}ERR: Period should be a number.{Style.RESET_ALL}")
            continue

        if period not in day_data:
            print(f"{Fore.RED}ERR: No subject found in Period {period}{Style.RESET_ALL}")
            continue

        print(f"Remove {day_data[period]} from Period {period}? (Y/N)")
        confrim = input(f"{Fore.CYAN}> {Style.RESET_ALL}").upper().strip()

        if confrim != "Y":
            print(f"{Fore.GREEN}Operation cancelled.{Style.RESET_ALL}")
            return
        
        removed_subject = day_data.pop(period)
        save_data(data)

        print(f"{Fore.GREEN}Removed {removed_subject} from {day}, Period {period}!{Style.RESET_ALL}")

        more = input(f"Would you like to add more? (Y/N){Fore.CYAN} > {Style.RESET_ALL}").upper().strip()
        
        if more != "Y":
            break