"""utils.py - reusable helper functions (display, input validation, passwords).

Business rules belong in models.py and SQL belongs in database.py,
so this file only contains small, general-purpose helpers.
"""

import getpass
import hashlib
import hmac
import os
import re
from datetime import datetime

LINE_WIDTH = 60
PBKDF2_ITERATIONS = 100_000  # more iterations = slower for attackers to guess


# ----------------------------------------------------------------------
# Display helpers
# ----------------------------------------------------------------------
def display_header(title):
    """Print a title between two separator lines."""
    print()
    print("=" * LINE_WIDTH)
    print(title.center(LINE_WIDTH))
    print("=" * LINE_WIDTH)


def display_messages(*messages):
    """Print any number of messages, one per line.

    *args is used because the caller may have one message or many
    (for example a title plus several detail lines), and we do not
    want to force them to build a list first.
    """
    for message in messages:
        print(message)


def create_log_message(**kwargs):
    """Build a one-line summary from keyword arguments.

    **kwargs is used because different actions report different details
    (action, tracking number, staff name, ...). Example:
    create_log_message(action="Assigned", tracking_number="AMS-00001")
    -> "[DONE] action=Assigned | tracking_number=AMS-00001"
    """
    parts = []
    for key, value in kwargs.items():
        parts.append(f"{key}={value}")
    return "[DONE] " + " | ".join(parts)


def pause_screen():
    """Wait for the user so they can read the output."""
    input("\nPress Enter to continue...")


def _shorten(text, max_width):
    """Cut long text so table columns stay neat."""
    text = str(text)
    if len(text) > max_width:
        return text[: max_width - 3] + "..."
    return text


def print_table(headers, rows, max_width=22):
    """Print a simple table. 'headers' is a list, 'rows' is a list of lists."""
    widths = []
    for column_index, header in enumerate(headers):
        longest = len(header)
        for row in rows:
            longest = max(longest, len(_shorten(row[column_index], max_width)))
        widths.append(longest)

    header_line = " | ".join(
        header.ljust(widths[index]) for index, header in enumerate(headers)
    )
    print(header_line)
    print("-" * len(header_line))
    for row in rows:
        cells = [
            _shorten(value, max_width).ljust(widths[index])
            for index, value in enumerate(row)
        ]
        print(" | ".join(cells))


# ----------------------------------------------------------------------
# Input helpers
# ----------------------------------------------------------------------
def get_non_empty_input(prompt, max_length=None):
    """Keep asking until the user types something that is not blank."""
    while True:
        value = input(prompt).strip()
        if value == "":
            print("This field cannot be empty.")
            continue  # ask again
        if max_length is not None and len(value) > max_length:
            print(f"Please use at most {max_length} characters.")
            continue
        return value


def get_optional_input(prompt):
    """Return what the user typed (may be an empty string)."""
    return input(prompt).strip()


def get_password_input(prompt="Password: "):
    """Read a password without showing it on the screen."""
    return getpass.getpass(prompt)


def validate_choice(choice, valid_choices):
    """Return True if 'choice' is one of 'valid_choices'."""
    return choice in valid_choices


def safe_int_input(prompt, min_value, max_value):
    """Ask for a whole number between min_value and max_value (inclusive)."""
    while True:
        raw_text = input(prompt).strip()
        try:
            number = int(raw_text)  # type casting: str -> int
        except ValueError:
            print("Please enter a valid number.")
            continue

        if not validate_choice(number, range(min_value, max_value + 1)):
            print(f"Please choose a number from {min_value} to {max_value}.")
            continue
        return number


def choose_from_list(title, options):
    """Show a numbered list and return the option the user picked."""
    print(f"\n{title}")
    for number, option in enumerate(options, start=1):
        print(f"  {number}. {option}")
    picked_number = safe_int_input("Enter choice: ", 1, len(options))
    return options[picked_number - 1]


# ----------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------
def validate_username(username):
    """Return (is_valid, message). 4-20 letters, numbers or underscores."""
    if re.fullmatch(r"[A-Za-z0-9_]{4,20}", username) is None:
        return False, "Username must be 4-20 characters: letters, numbers, underscore."
    return True, ""


def validate_password(password):
    """Return (is_valid, message). At least 8 characters with a letter and a digit."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    has_letter = any(character.isalpha() for character in password)
    has_digit = any(character.isdigit() for character in password)
    if not (has_letter and has_digit):
        return False, "Password must contain at least one letter and one number."
    return True, ""


# ----------------------------------------------------------------------
# Passwords (PBKDF2 from Python's standard library)
# ----------------------------------------------------------------------
def hash_password(password, salt=None):
    """Return "salt_hex$hash_hex".

    1. A random salt is created so two users with the same password
       get different hashes.
    2. PBKDF2 mixes the password and salt many times (slow on purpose).
    3. We store the salt together with the hash so we can check later.
    """
    if salt is None:
        salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS
    )
    return f"{salt.hex()}${digest.hex()}"


def verify_password(password, stored_hash):
    """Hash the typed password with the stored salt and compare."""
    try:
        salt_hex, _ = stored_hash.split("$")
        salt = bytes.fromhex(salt_hex)
    except ValueError:
        return False  # stored value is not in the expected format
    new_hash = hash_password(password, salt)
    return hmac.compare_digest(new_hash, stored_hash)


# ----------------------------------------------------------------------
# Formatting
# ----------------------------------------------------------------------
def generate_tracking_number(complaint_id):
    """Turn a database ID into a tracking number: 1 -> 'AMS-00001'."""
    return f"AMS-{complaint_id:05d}"


def format_date(value, include_time=False):
    """Format a datetime for display; return 'N/A' when there is none."""
    if not isinstance(value, datetime):
        return "N/A"
    if include_time:
        return value.strftime("%b %d, %Y %I:%M %p")
    return value.strftime("%b %d, %Y")
