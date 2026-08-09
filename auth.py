accounts = {
    "admin": "1234",
    "allen": "password123",
    "student": "qwerty"
}

username = input("Username: ")
password = input("Password: ")

if username in accounts and accounts[username] == password:
    print("Login successful!")
else:
    print("Invalid username or password.")

