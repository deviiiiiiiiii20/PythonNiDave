
from tkinter import *
from tkinter import messagebox

import atm_backend

# ---------- Global state ----------
current_username = None
current_result = None  # full row from userinfo (id, username, password, balance)

# ---------- Window setup ----------
window = Tk()
window.geometry("500x500")
window.title("ATM SYSTEM")


def clear_window():
    for widget in window.winfo_children():
        widget.destroy()


# ---------- Screens ----------

def show_login():
    clear_window()
    global nameEntry, passwordEntry, resultLabel

    Label(window, text="ATM SYSTEM", font=("Arial", 25, "bold")).pack(pady=20)

    Label(window, text="Username:", font=("Arial", 10)).place(x=100, y=100)
    nameEntry = Entry(window, width=25)
    nameEntry.place(x=200, y=100)

    Label(window, text="Password:", font=("Arial", 10)).place(x=100, y=130)
    passwordEntry = Entry(window, width=25, show="*")
    passwordEntry.place(x=200, y=130)

    resultLabel = Label(window, text="", font=("Arial", 10, "bold"))
    resultLabel.place(x=100, y=160)

    Button(window, text="Login", width=12, command=login_click).place(x=140, y=220)
    Button(window, text="Register", width=12, command=show_register).place(x=260, y=220)
    Button(window, text="Exit", width=12, command=window.destroy).place(x=200, y=260)


def login_click():
    global current_username, current_result

    username = nameEntry.get().strip()
    password = passwordEntry.get().strip()

    if not username or not password:
        resultLabel.config(text="Please fill in both fields.", fg="red")
        return

    result = atm_backend.do_login(username, password)
    if result:
        current_username = username
        current_result = result
        show_dashboard()
    else:
        resultLabel.config(text="Invalid username or password.", fg="red")


def show_register():
    clear_window()
    global regNameEntry, regPassEntry, regResultLabel

    Label(window, text="REGISTER", font=("Arial", 25, "bold")).pack(pady=20)

    Label(window, text="Username:", font=("Arial", 10)).place(x=100, y=100)
    regNameEntry = Entry(window, width=25)
    regNameEntry.place(x=200, y=100)

    Label(window, text="Password:", font=("Arial", 10)).place(x=100, y=130)
    regPassEntry = Entry(window, width=25, show="*")
    regPassEntry.place(x=200, y=130)

    regResultLabel = Label(window, text="", font=("Arial", 10, "bold"))
    regResultLabel.place(x=100, y=160)

    Button(window, text="Create Account", width=14, command=register_click).place(x=150, y=220)
    Button(window, text="Back to Login", width=14, command=show_login).place(x=280, y=220)


def register_click():
    username = regNameEntry.get().strip()
    password = regPassEntry.get().strip()

    if not username or not password:
        regResultLabel.config(text="Please fill in both fields.", fg="red")
        return

    created = atm_backend.do_register(username, password)
    if created:
        messagebox.showinfo("Success", "Account created successfully!")
        show_login()
    else:
        regResultLabel.config(text="Username already taken.", fg="red")


def show_dashboard():
    clear_window()
    global balanceLabel, logBox

    Label(window, text=f"Welcome, {current_username}!", font=("Arial", 20, "bold")).pack(pady=15)

    balance = atm_backend.get_balance(current_result[0])
    balanceLabel = Label(window, text=f"Balance: {balance}", font=("Arial", 14))
    balanceLabel.pack(pady=5)

    Button(window, text="Deposit", width=12, command=show_deposit).pack(pady=5)
    Button(window, text="Withdraw", width=12, command=show_withdraw).pack(pady=5)

    Label(window, text="Transaction Log:", font=("Arial", 10, "bold")).pack(pady=(15, 0))
    logBox = Text(window, width=45, height=10)
    logBox.pack(pady=5)
    logBox.config(state=DISABLED)

    Button(window, text="Logout", width=12, command=show_login).pack(pady=10)


def log_transaction(message):
    logBox.config(state=NORMAL)
    logBox.insert(END, message + "\n")
    logBox.config(state=DISABLED)


def show_deposit():
    clear_window()
    global depositEntry, depositResultLabel

    Label(window, text="DEPOSIT", font=("Arial", 20, "bold")).pack(pady=20)
    Label(window, text="Amount:", font=("Arial", 10)).pack()
    depositEntry = Entry(window, width=20)
    depositEntry.pack(pady=5)

    depositResultLabel = Label(window, text="", font=("Arial", 10, "bold"))
    depositResultLabel.pack(pady=5)

    Button(window, text="Confirm", width=12, command=deposit_click).pack(pady=5)
    Button(window, text="Back", width=12, command=show_dashboard).pack(pady=5)


def deposit_click():
    amount_text = depositEntry.get().strip()
    try:
        amount = float(amount_text)
        if amount <= 0:
            depositResultLabel.config(text="Amount must be greater than 0.", fg="red")
            return
    except ValueError:
        depositResultLabel.config(text="Please enter a valid number.", fg="red")
        return

    new_balance = atm_backend.do_deposit(current_result[0], amount)
    show_dashboard()
    log_transaction(f"Deposited {amount} | New balance: {new_balance}")


def show_withdraw():
    clear_window()
    global withdrawEntry, withdrawResultLabel

    Label(window, text="WITHDRAW", font=("Arial", 20, "bold")).pack(pady=20)
    Label(window, text="Amount:", font=("Arial", 10)).pack()
    withdrawEntry = Entry(window, width=20)
    withdrawEntry.pack(pady=5)

    withdrawResultLabel = Label(window, text="", font=("Arial", 10, "bold"))
    withdrawResultLabel.pack(pady=5)

    Button(window, text="Confirm", width=12, command=withdraw_click).pack(pady=5)
    Button(window, text="Back", width=12, command=show_dashboard).pack(pady=5)


def withdraw_click():
    amount_text = withdrawEntry.get().strip()
    try:
        amount = float(amount_text)
    except ValueError:
        withdrawResultLabel.config(text="Please enter a valid number.", fg="red")
        return

    new_balance, error = atm_backend.do_withdraw(current_result[0], amount)
    if error:
        withdrawResultLabel.config(text=error, fg="red")
        return

    show_dashboard()
    log_transaction(f"Withdrew {amount} | New balance: {new_balance}")


if __name__ == "__main__":
    show_login()
    window.mainloop()