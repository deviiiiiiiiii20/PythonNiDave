import hashlib


def show_header(title):
    print()
    print("=" * 50)
    print(title.center(50))
    print("=" * 50)


def pause():
    input("\nPress Enter to continue...")


def get_text(prompt):
    while True:
        text = input(prompt).strip()
        if text == "":
            print("Please type something.")
            continue
        return text


def get_number(prompt, low, high):
    while True:
        text = input(prompt).strip()
        if not text.isdigit():
            print("Please enter a number.")
            continue
        number = int(text)
        if number < low or number > high:
            print("Choose a number from", low, "to", high)
            continue
        return number


def choose_from_list(title, items):
    print()
    print(title)
    number = 1
    for item in items:
        print(f"{number}. {item}")
        number += 1
    choice = get_number("Enter choice: ", 1, len(items))
    return items[choice - 1]


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def make_tracking_number(number):
    # 1 becomes AMS-00001
    return "AMS-" + str(number).zfill(5)


def format_date(value):
    if value is None:
        return "N/A"
    return value.strftime("%b %d, %Y %I:%M %p")
