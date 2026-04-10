import data
from datetime import timedelta
from colorama import init, Fore, Style

init(autoreset=True)

def extract_subjects(day_data):
    """Handles both dict (period→subject) and list formats"""
    if isinstance(day_data, dict):
        return set(day_data.values())
    return set(day_data)

def get_books(subjects, books):
    book_set = set()
    for sub in subjects:
        for b in books.get(sub, {}).values():
            book_set.add(b)
    return book_set

def print_list(title, items, color):
    print(f"\n{color}{title}:{Style.RESET_ALL}")
    if items:
        print("\n".join(f"- {i}" for i in items))
    else:
        print(f"{Style.DIM}Nothing{Style.RESET_ALL}")

def format_subjects(subjects):
    return ", ".join(subjects) if subjects else f"{Style.DIM}None{Style.RESET_ALL}"

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
        print(f"{Fore.YELLOW}No school today{Style.RESET_ALL}")
        return

    today_subjects = extract_subjects(timetable.get(data.today_name, {}))
    yesterday_subjects = extract_subjects(timetable.get(yesterday_name, {}))

    if not today_subjects:
        print(f"{Fore.RED}ERR: No subjects today{Style.RESET_ALL}")
        return

    sub_remove = yesterday_subjects - today_subjects
    sub_add = today_subjects - yesterday_subjects
    sub_keep = today_subjects & yesterday_subjects

    today_books = get_books(today_subjects, books)
    yesterday_books = get_books(yesterday_subjects, books)

    book_remove = yesterday_books - today_books
    book_add = today_books - yesterday_books
    book_keep = today_books & yesterday_books

    print(f"\n{Fore.CYAN}Yesterday:{Style.RESET_ALL} {yesterday_name}")
    print(f"{Fore.CYAN}Today:{Style.RESET_ALL} {data.today_name}")

    print(f"\n{Style.BRIGHT}Subject Changes{Style.RESET_ALL}")
    print(f"{Fore.RED}Remove:{Style.RESET_ALL} {format_subjects(sub_remove)}")
    print(f"{Fore.GREEN}Add:{Style.RESET_ALL} {format_subjects(sub_add)}")
    print(f"{Fore.YELLOW}Keep:{Style.RESET_ALL} {format_subjects(sub_keep)}")

    print(f"\n{Style.BRIGHT}Book Changes{Style.RESET_ALL}")
    print_list("Remove from bag", book_remove, Fore.RED)
    print_list("Add to bag", book_add, Fore.GREEN)
    print_list("Keep in bag", book_keep, Fore.YELLOW)

    confirm = input(f"\nUpdate bag with today's books? (Y/N){Fore.CYAN} > {Style.RESET_ALL}").upper().strip()

    if confirm == "Y":
        update_bag(app_data, user_data, today_books)
    else:
        print(f"{Fore.YELLOW}{Style.DIM}Bag not updated.{Style.RESET_ALL}")

def show_tomorrow_plan(app_data, user_data):
    timetable = user_data["timetable"]
    books = user_data["books"]

    if data.tomorrow_name not in timetable:
        print(f"{Fore.YELLOW}No school tomorrow ({data.tomorrow_name}){Style.RESET_ALL}")
        return

    today_subjects = extract_subjects(timetable.get(data.today_name, {}))
    tomorrow_subjects = extract_subjects(timetable.get(data.tomorrow_name, {}))

    if not tomorrow_subjects:
        print(f"{Fore.RED}ERR: No subjects for {data.tomorrow_name}{Style.RESET_ALL}")
        return

    sub_remove = today_subjects - tomorrow_subjects
    sub_add = tomorrow_subjects - today_subjects
    sub_keep = today_subjects & tomorrow_subjects

    today_books = get_books(today_subjects, books)
    tomorrow_books = get_books(tomorrow_subjects, books)

    book_remove = today_books - tomorrow_books
    book_add = tomorrow_books - today_books
    book_keep = today_books & tomorrow_books

    print(f"\n{Fore.CYAN}Today:{Style.RESET_ALL} {data.today_name}")
    print(f"{Fore.CYAN}Tomorrow:{Style.RESET_ALL} {data.tomorrow_name}")

    print(f"\n{Style.BRIGHT}Subject Changes{Style.RESET_ALL}")
    print(f"{Fore.RED}Remove:{Style.RESET_ALL} {format_subjects(sub_remove)}")
    print(f"{Fore.GREEN}Add:{Style.RESET_ALL} {format_subjects(sub_add)}")
    print(f"{Fore.YELLOW}Keep:{Style.RESET_ALL} {format_subjects(sub_keep)}")

    print(f"\n{Style.BRIGHT}Book Changes{Style.RESET_ALL}")
    print_list("Remove from bag", book_remove, Fore.RED)
    print_list("Add to bag", book_add, Fore.GREEN)
    print_list("Keep in bag", book_keep, Fore.YELLOW)

    print(f"\n{Fore.GREEN}Pack your bag for tomorrow today!{Style.RESET_ALL}")

    confirm = input(f"\nPrepare bag now? (Y/N){Fore.CYAN}> {Style.RESET_ALL}").upper().strip()

    if confirm == "Y":
        update_bag(app_data, user_data, tomorrow_books)
    else:
        print(f"{Fore.YELLOW}{Style.DIM}Bag not updated.{Style.RESET_ALL}")