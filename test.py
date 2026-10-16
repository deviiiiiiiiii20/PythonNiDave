

items = []
while True:
    print(" ")
    print("1. Input item")
    print("2. Exit")
    user = input("Enter your choice: ")

    if user == "1":
        item = input("Enter your the item: ")
        items.append(item)

    elif user == "2":
        count = 1
        for value in items:
            print(f'{count}. {value}')
            count += 1
        exit()
    else:
        print("Invalid choice")
        break