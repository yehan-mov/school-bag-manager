#region Libaries
import data, utils, usermenu
from datetime import timedelta
from colorama import init, Fore, Style
#endregion

init(autoreset = True)

def update_bag(app_data, user_data, new_books):
    user_data["bag"] = list(new_books)
    data.save_data(app_data)
    print(f"{Fore.GREEN}Bag updated and saved!{Style.RESET_ALL}")

def show_today_plan(app_data, user_data):
    timetable = user_data["timetable"]
    books = user_data["books"]

    yesterday = data.today - timedelta(days=1)
    yesterday_name = yesterday.strftime("%A")

    if data.today_name not in timetable:
        print(f"{Fore.YELLOW}No school today{Style.RESET_ALL}]")
        return
    
    today_subjects = set(timetable.get(data.today_name, []))
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

    print(f"\n{Fore.CYAN}Yesterday:{Style.RESET_ALL} {yesterday_name}")
    print(f"{Fore.CYAN}Today:{Style.RESET_ALL} {data.today_name}")

    print(f"\n{Style.BRIGHT}Subject Changes{Style.RESET_ALL}")
    print(f"{Fore.RED}Remove:{Style.RESET_ALL}", list(sub_remove) if sub_remove else f"{Style.DIM}]None{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Add:{Style.RESET_ALL}", list(sub_add) if sub_add else f"{Style.DIM}None{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Keep:{Style.RESET_ALL}", list(sub_keep) if sub_keep else f"{Style.DIM}None{Style.RESET_ALL}")

    print(f"\n{Style.BRIGHT}Book Changes{Style.RESET_ALL}")

    print(f"\n{Fore.RED}Remove from bag:{Style.RESET_ALL}")
    print("\n".join(f"- {b}" for b in book_remove) if book_remove else f"{Style.RESET_ALL}Nothing{Style.RESET_ALL}")

    print(f"\n{Fore.GREEN}Add to bag:{Style.RESET_ALL}")
    print("\n".join(f"- {b}" for b in book_add) if book_add else f"{Style.DIM}Nothing{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}Keep in bag:{Style.RESET_ALL}")
    print("\n".join(f"- {b}" for b in book_keep) if book_keep else f"{Style.DIM}Nothing{Style.RESET_ALL}")

    confirm = input(f"\nUpdate bag with today's books? (Y/N){Fore.CYAN} > {Style.RESET_ALL}").upper().strip()

    if confirm == "Y":
        update_bag(user_data, today_books)
    else:
        print(f"{Fore.YELLOW}{Style.DIM}Bag not updated.{Style.RESET_ALL}")

def show_tomorrow_plan(app_data, user_data):
    timetable = user_data["timetable"]
    books = user_data["books"]

    if data.tomorrow_name not in timetable:
        print(f"{Fore.YELLOW}No school tomorrow ({data.tomorrow_name}){Style.RESET_ALL}")
        return
    
    today_subjects = set(timetable.get(data.today_name, []))
    tomorrow_subjects = set(timetable.get(data.tomorrow_name, []))

    if not tomorrow_subjects:
        print(f"{Fore.RED}ERR: No subjects for {data.tomorrow_name}{Style.RESET_ALL}")
        return
    
    sub_remove = today_subjects - tomorrow_subjects
    sub_add = tomorrow_subjects - today_subjects
    sub_keep = today_subjects & tomorrow_subjects

    def get_books(subjects):
        book_set = set()
        for sub in subjects:
            for b in books.get(sub, {}).values():
                book_set.add(b)
        return book_set
    
    today_books = get_books(today_subjects)
    tomorrow_books = get_books(tomorrow_subjects)

    book_remove = today_books - tomorrow_books
    book_add = tomorrow_books - today_books
    book_keep = today_books & tomorrow_books

    print(f"\n{Fore.CYAN}Today:{Style.RESET_ALL} {data.today_name}")
    print(f"{Fore.CYAN}Tomorrow:{Style.RESET_ALL} {data.tomorrow_name}")

    print(f"\n{Style.BRIGHT}Subject Changes{Style.RESET_ALL}")
    print(f"{Fore.RED}Remove:{Style.RESET_ALL}", list(sub_remove) if sub_remove else f"{Style.DIM}None{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Add:{Style.RESET_ALL}", list(sub_add) if sub_add else f"{Style.DIM}None{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Keep:{Style.RESET_ALL}]", list(sub_keep) if sub_keep else f"{Style.DIM}None{Style.RESET_ALL}")

    print(f"\n{Style.BRIGHT}Book Changes{Style.RESET_ALL}")

    print(f"\n{Fore.RED}Remove from bag:{Style.RESET_ALL}")
    print("\n".join(f"- {b}" for b in book_remove) if book_remove else f"{Style.DIM}Nothing{Style.RESET_ALL}")

    print(f"\n{Fore.GREEN}Add to bag:{Style.RESET_ALL}")
    print("\n".join(f"- {b}" for b in book_add) if book_add else f"{Style.DIM}Nothing{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}Keep in bag:{Style.RESET_ALL}")
    print("\n".join(f"- {b}" for b in book_keep) if book_keep else f"{Style.DIM}Nothing{Style.RESET_ALL}")

    print(f"\n{Fore.GREEN}Pack your bag for tomorrow today!{Style.RESET_ALL}")

    confirm = input(f"\nPrepare bag now? (Y/N){Fore.CYAN}> {Style.RESET_ALL}").upper().strip()

    if confirm == "Y":
        update_bag(user_data, tomorrow_books)
    else:
        print(f"{Fore.YELLOW}{Style.DIM}Bag not updated.{Style.RESET_ALL}")