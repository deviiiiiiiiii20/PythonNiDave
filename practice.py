grades = []

def enterGrade():
    while True:
        grade = input("Enter a grade: ")
        if grade ==  "done":
            print(grades)
            menu()
            break
        grades.append(float(grade))

    average = sum(grades) / len(grades)

    print(f"Average Grade: {average}" )

def seeGrade():
    check = input("Enter a student number: ")

    if int(check) <= len(grades):
        print(grades[int(check)])
    else:
        print("INVALID")


def menu():
    while True:
        print("1. Enter a grade")

        print("2. See grade")

        choice = input("Enter your choice: ")
        if choice == "1":
            enterGrade()
        if choice == "2":
            seeGrade()
        else:
            exit()

menu()