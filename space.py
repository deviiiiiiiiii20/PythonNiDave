names = []

for i in range(1, 5):
    name = input("Enter your name: ")
    if name == "stop":
        print(names)
        break
    names.append(name)

print(f"There are {len(names)} numbers of name. ")