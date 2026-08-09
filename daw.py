balance = 0


def basta():
    num1 = int(input("Enter first number: "))
    num2 = int(input("Enter second number: "))
    return num1, num2


def engk(num1, num2):
    sum = num1 + num2
    dif = num1 - num2
    print(f"Sum: {sum}, Difference: {dif}")


def nyak():
    while True:
        num1, num2 = basta()
        engk(num1, num2)
        choice = input("Do you want to continue? ")
        if choice != "yes":
            break


if __name__ == "__main__":
    nyak()