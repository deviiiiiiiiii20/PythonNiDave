from tkinter import *
window = Tk()
window.geometry("500x500")
window.title("GUI PRACTICE")

nameEntry = StringVar()
passwordEntry = StringVar()

accounts = {
    'allendave': 'allendave123'
}
def clearWindow():
    for widget in window.winfo_children():
        widget.destroy()

def login():
    userWrote = nameEntry.get()
    passwordWrote = passwordEntry.get()

    if userWrote in accounts and accounts[userWrote] == passwordWrote:
        page2()
    else:
        print(f"Invalid username or password")










def page2():
    clearWindow()

    welcome = Label(window, text="WELCOME TO DASHBOARD", font = ("Arial", 25, 'bold'))
    welcome.pack()

    chatBox = Text(window, width=40, height=15)
    chatBox.pack(pady=10)

    entry = Entry(window, width=30)
    entry.pack()

    def send_message():
        msg = entry.get()
        chatBox.insert(END, msg + "\n")  # adds text at the end, then a newline
        entry.delete(0, END)  # clears the entry box after sending

    sendBtn = Button(window, text="Send", command=send_message)
    sendBtn.pack(pady=5)












def quit():
    window.destroy()

label1 = Label(window, text="ATM SYSTEM", font = ("Arial", 25, 'bold'))
label1.pack()

name = Label(window, text="Username: ", font = ("Arial", 10))
name.pack()
name.place(x=20, y=50)

nameEntry = Entry(window, width=30)
nameEntry.pack()
nameEntry.place(x=95, y=50)

password = Label(window, text="Password: ", font = ("Arial", 10))
password.pack()
password.place(x=20, y=75)

passwordEntry = Entry(window, width=30)
passwordEntry.pack()
passwordEntry.place(x=95, y=75)


button1 = Button(window, text="login", width=12, relief = 'groove', command= login,font =("Arial", 10 ))
button1.pack()
button1.place(x=140, y= 370)

button2 = Button(window, text="Exit", width=12, relief = 'groove', command= quit,font =("Arial", 10 ))
button2.pack()
button2.place(x=260, y=370)

window.mainloop()