#region Libaires
import json, os, sys
from datetime import datetime, timedelta
from colorama import Fore, Style
#endregion

#region File & Time Mangement
def get_db_path():
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), "database.json")
    else:
        return "database.json"
    
DB_FILE = get_db_path()

today = datetime.now()
today_name = today.strftime("%A")

tomorrow = today + timedelta(days = 1)
tomorrow_name = tomorrow.strftime("%A")
#endregion

#region Data mangement
def load_data():
    default_data = {"users": {}}
    
    try:
        with open(DB_FILE, "r", encoding = "utf-8") as f:
            content = f.read().strip()

            if not content:
                print(f"{Fore.YELLOW}Database empty. Intializing...{Style.RESET_ALL}")
                save_data(default_data)
                return default_data
            
            return json.loads(content)
        
    except FileNotFoundError:
        print(f"{Fore.YELLOW}Databse not found. Creating new one...{Style.RESET_ALL}")
        save_data(default_data)
        return default_data
    
    except json.JSONDecodeError:
        print(f"{Fore.RED}Database corrupted. Resetting...{Style.RESET_ALL}")
        save_data(default_data)
        return default_data
    
def save_data(data):
    with open(DB_FILE, "w", encoding = "utf-8") as f:
        json.dump(data, f, indent = 4)
#endregion

#region System functions
def clear():
    os.system("cls" if os.name == "nt" else "clear")
#endregion

#region Adding data
def add_user(data):
    username = input(f"Enter new username{Fore.CYAN}> {Style.RESET_ALL}").strip()

    if username in data["users"]:
        print(f"{Fore.RED}ERR: User already exists{Style.RESET_ALL}")
        return
    
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
    print(f"{Fore.GREEN}User added succesfully!{Style.RESET_ALL}")

def add_subject(user_data):
    subject = input(f"Enter subject name{Fore.CYAN}> {Style.RESET_ALL}").strip()

    if not subject:
        print(f"{Fore.RED}ERR: Subject name cannot be empty{Style.RESET_ALL}")
        return
    
    if subject in user_data["books"]:
        print(f"{Fore.RED}ERR: Subject already exists{Style.RESET_ALL}")
        return
    
    user_data["books"][subject] = {
        "textbook": f"{subject} Textbook",
        "notebook": f"{subject} Notebook"
    }

    save_data(data)

    print(f"{Fore.GREEN}Subject '{subject}' added!{Style.RESET_ALL}")

def add_to_timetable(user_data):
    day = input(f"Enter day (Monday-Friday){Fore.CYAN}> {Style.RESET_ALL}").strip()

    if day not in user_data["timetable"]:
        print(f"{Fore.RED}ERR: Invalid day{Style.RESET_ALL}")
        return
    
    subject = input(f"Enter subject to add{Fore.CYAN}> {Style.RESET_ALL}").strip()

    if subject not in user_data["books"]:
        print(f"{Fore.RED}ERR: Subject not found in books{Style.RESET_ALL}")
        return
    
    user_data["timetable"][day].append(subject)
    save_data(data)

    print(f"{Fore.GREEN}Added to timetable!{Style.RESET_ALL}")
#endregion

#region Core Logic
def get_books(subjects, books):
    book_set = set()
    
    for subject in subjects:
        for book in books.get(subject, {}).values():
            book_set.add(book)
    return book_set

def update_bag(user_data, new_books):
    user_data["bag"] = list(new_books)
    save_data(data)
    print(f"{Fore.GREEN}Bag updated and saved!{Style.RESET_ALL}")

def show_today_plan(user_data):
    timetable = user_data["timetable"]
    books = user_data["books"]

    yesterday = today - timedelta(days = 1)
    yesterday_name = yesterday.strftime("%A")

    if today_name not in timetable:
        print("No school today")
        return
    
    today_subjects = set(timetable.get(today_name, []))
    yesterday_subjects = set(timetable.get(yesterday_name, []))

    if not today_subjects:
        print(f"{Fore.RED}ERR: No subjects today{Style.RESET_ALL}")
        return
    
    sub_remove = yesterday_subjects - today_subjects
    sub_add = today_subjects - yesterday_subjects
    sub_keep = today_subjects & yesterday_subjects

    def get_books(subjects):
        book_set = set()
        for sub in subjects:
            for b in books.get(sub, {}).values():
                book_set.add(b)
        return book_set
    
    today_books = get_books(today_subjects)
    yesterday_books = get_books(yesterday_subjects)

    book_remove = yesterday_books - today_books
    book_add = today_books - yesterday_books
    book_keep = today_books & yesterday_books

    print(f"\nYesterday: {yesterday_name}")
    print(f"\nToday: {today_name}")

    print("\nSubjects Changes")
    print("Remove:", list(sub_remove) if sub_remove else "None")
    print("Add:", list(sub_add) if sub_add else "None")
    print("Keep:", list(sub_keep) if sub_add else "None")

    print("\nBook Changes")

    print("\nRemove from bag:")
    print("\n".join(f"- {b}" for b in book_remove) if book_remove else "Nothing")

    print("\nAdd to bag:")
    print("\n".join(f"- {b}" for b in book_add) if book_add else "Nothing")

    print("\nKeep in bag:")
    print("\n".join(f"- {b}" for b in book_keep) if book_keep else "Notthing")

    confrim = input(f"\nUpdate bag with today's book? (Y/N) {Fore.CYAN}> {Style.RESET_ALL}").upper()

    if confrim == "Y":
        update_bag(user_data, today_books)
    else:
        print(f"{Fore.YELLOW}Bag not updated.{Style.RESET_ALL}")

def show_tomorrow_plan(user_data):
    timetable = user_data["timetable"]
    books = user_data["books"]

    tomorrow = today + timedelta(days = 1)
    tomorrow_name = tomorrow.strftime("%A")

    if tomorrow_name not in timetable:
        print(f"{Fore.YELLOW}Maybe no school tomorrow ({tomorrow_name}){Style.RESET_ALL}")
        return
    
    today_subjects = set(timetable.get(today_name, []))
    tomorrow_subjects = set(timetable.get(tomorrow_name, []))

    if not tomorrow_subjects:
        print(f"{Fore.RED}ERR: No subejcts for {tomorrow_name}{Style.RESET_ALL}")
        return
    
    sub_remove = today_subjects - tomorrow_subjects
    sub_add = tomorrow_subjects - today_subjects
    sub_keep = today_subjects & tomorrow_subjects

    def get_books(subjects):
        book_set = set()
        for sub in subjects:
            if sub not in books:
                print(f"{Fore.YELLOW}WARNING: '{sub}' not found in books{Style.RESET_ALL}")
                continue
            for b in books[sub].values():
                book_set.add(b)
        return book_set
    
    today_books = get_books(today_subjects)
    tomorrow_books = get_books(tomorrow_subjects)

    book_remove = today_books - tomorrow_books
    book_add = tomorrow_books - today_books
    book_keep = today_books & tomorrow_books

    print(f"\nToday: {today_name}")
    print(f"Tomorrow: {tomorrow_name}")

    print("\nSubject changes (Pack for Tomorrow)")
    print("Remove:", list(sub_remove) if sub_remove else "None")
    print("Add:", list(sub_add) if sub_add else "None")
    print("Keep:", list(sub_keep) if sub_keep else "None")

    print("\nBook changes (Pack Tonight)")

    print("\nRemove from bag (not needed tomorrow):")
    print("\n".join(f"- {b}" for b in book_remove) if book_remove else "Nothing")

    print("\nAdd to bag (needed tomorrow):")
    print("\n".join(f"- {b}" for b in book_add) if book_add else "Nothing")

    print("\nKeep in bag:")
    print("\n".join(f"- {b}" for b in book_keep) if book_keep else "Nothing")

    print(f"\n{Fore.GREEN}Pack your bag for tomorrow today!{Style.RESET_ALL}")

    confirm = input(f"\nPrepare bag for tomorrow now? (Y/N){Fore.CYAN}> {Style.RESET_ALL}")

    if confirm == "Y":
        update_bag(user_data, tomorrow_books)
    else:
        print(f"{Fore.YELLOW}Bag not updated.{Style.RESET_ALL}")

def user_menu(username, user_data):
    while True:
        print(f"\nHello {username}! Please select a option.")
        print("[1] Show today's plan")
        print("[2] Show tomorrow's plan")
        print("[3] Add subject")
        print("[4] Add to timetable")
        print("[5] Back")

        try:
            choice = int(input(f"{Fore.CYAN}> {Style.RESET_ALL}"))
        except ValueError:
            continue

        if choice == 1:
            show_today_plan(user_data)
        
        elif choice == 2:
            show_tomorrow_plan(user_data)

        elif choice == 3:
            add_subject(user_data)

        elif choice == 4:
            add_to_timetable(user_data)

        elif choice == 5:
            return
        
        else:
            print(f"{Fore.RED}ERR: Invaild option selected! Please try again.{Style.RESET_ALL}")
            continue
#endregion

#region Main
def main():
    global data
    data = load_data()
    clear()

    while True:
        print("\nSchool bag mangement")
        print("[1] Select user")
        print("[2] Add user")
        print("[0] Exit")

        try:
            choice = int(input(f"{Fore.CYAN}> {Style.RESET_ALL}"))
        except ValueError:
            continue

        if choice == 0:
            break

        elif choice == 2:
            add_user(data)

        elif choice == 1:
            if not data["users"]:
                print("No users found")
                continue

            print("\nUsers:")
            users = list(data["users"].keys())
            for i, u in enumerate(users, 1):
                print(f"[{i}] {u}")

            try:
                u_choice = int(input(f"{Fore.CYAN}> {Style.RESET_ALL}"))
                username = users[u_choice - 1]
            except:
                print(f"{Fore.RED}ERR: Invalid selection{Style.RESET_ALL}")
                continue

            user_menu(username, data["users"[username]])

if __name__ == "__main__":
    main()
#endregion