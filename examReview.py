
while True:
    password = input("Enter a password to check: ")

    has_upper = False
    has_lower = False
    has_digit = False

    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True

    has_min_length = len(password) >= 8

    if has_min_length and has_upper and has_lower and has_digit:
        print("Password strength: STRONG")
    else:
        print("Password strength: WEAK")
        print("Missing requirements:")
        if has_min_length == False:
            print("- Minimum length of 8 characters")
        if not has_upper:
            print("- At least 1 uppercase letter")
        if not has_lower:
            print("- At least 1 lowercase letter")
        if not has_digit:
            print("- At least 1 numeric digit")
"""
def sumpUpTo(n):
    if n == 0:
        return 0
    else:
        return n * sumpUpTo(n - 1)

print(sumpUpTo(8))

"""