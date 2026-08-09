from selectors import SelectSelector
def guessThePassword():
    print("________________________________________________________________________"
          "______________________________________________________________________________________"
          "__________________________")
    print("CHALLENGE 1: GUESS THE PASSWORD")
    print("Direction: Enter a 4-digit code.")
    print("")
    print("Clue: birthday date of one of the member.")
    while True:
        password = input("Enter the password: ")
        if password == "1120":
            print(" ")
            print("Password is correct. 'November 20 (1120)' is the birthday date of Allen.")
            print("Status: Challenge 1 Completed. Proceeding to the next room.")
            print("________________________________________________________________________"
                  "______________________________________________________________________________________"
                  "__________________________")
            luckyNumber()
            break

def luckyNumber():
    print("________________________________________________________________________"
          "______________________________________________________________________________________"
          "__________________________")
    print("CHALLENGE 2: LUCKY NUMBER")
    print("Direction: Enter a carefully guessed 2 digit lucky number. You have 3 attempts. "
          "If you fail to guess the number after these attempts the domain will collapse.")
    print("Clue: Favorite number ng pinaka pogi (si Allen haha)")

    myLuckyNumber = "20"
    maxAttempts = 3

    for attempt in range(1, maxAttempts + 1):
        guess = input("Please enter your guessed lucky number: ")
        if guess == myLuckyNumber:
            print("")
            print("Lucky number is correct. '20' is the favorite number of allen.")
            print("Status: Challenge 2 Completed. Proceeding to the next room.")
            print("________________________________________________________________________"
                  "______________________________________________________________________________________"
                  "__________________________")
            facingDoors()
            break
        if attempt >= maxAttempts:
            print("")
            print("Maximum attempts reached. The domain is collapsing...")
            print("Game over. You Died.")
            print("________________________________________________________________________"
                  "______________________________________________________________________________________"
                  "__________________________")
            break

def facingDoors():
    print("________________________________________________________________________"
          "______________________________________________________________________________________"
          "__________________________")
    print("CHALLENGE 3: THE ROOM OF GEMS")
    print("Direction: Carefully pick a door to decide your future.")
    print("")
    print("Door 1: Emerald")
    print("Door 2: Amethyst")
    print("Door 3: Amber")
    door = input("Please enter your choice: ")

    if door == "Emerald" or door == "emerald" or  door == "1":
        print("")
        print("Successfully entered the Emerald room.")
        print("System notice: YOU FOUND THE TREASURE CHEST.")
        print("Warning: The server boss is in the room. Quickly pick a color to hide!! ")
        print(" ")
        print("Color choices: Green, Red, Black")
        color = input("Enter your choice: ")
        if color == "Green" or color == "green" or color == "GREEN":
            print("You have successfully acquired the treasure chest and cleared the domain. Congratulations!")
            print("The system has a final note for you. Would you like to open it? (YES / NO) ")
            action = input("Action: ")
            if action == "YES" or action == "Yes" or action == "yes":
                gameVictory()
            elif action == "NO" or action == "NO" or action == "no":
                print("Domain successfully cleared. CONGRATS ADVENTURER.")
            else:
                print("Invalid action")
                exit()
        elif color == "Red" or color == "red" or color == "RED":
            print("The boss found and killed you!")
            gameOver()
            exit()
        elif color == "Black" or color == "black" or color == "BLACK":
            print("The boss found and killed you!")
            gameOver()
            exit()
        else:
            print("Failed to pick a color from the given choices.")
            gameOver()
            exit()

    elif door == "Amethyst" or door == "amethyst" or door == "2":
        print("")
        print("You have successfully entered the Amethyst room.")
        print("Status: The server boss found and killed you...")
        gameOver()
        exit()

    elif door == "Amber" or door == "amber" or door == "3":
        print(" ")
        print("You have successfully acquired the treasure chest and cleared the domain. Congratulations!")
        print("The system has a final note for you. Would you like to open it? (YES / NO) ")
        action = input("Action: ")
        if action == "YES" or action == "Yes" or action == "yes":
            gameVictory()
        elif action == "NO" or action == "NO" or action == "no":
            print("Domain successfully cleared. CONGRATS ADVENTURER.")
        else:
            print("Invalid action")
            exit()

    else:
        print("Invalid action")
        exit()

def gameOver():
    print("Game over. Failed to conquer this domain.")

def gameVictory():
    print("")
    print("System, ")
    print("First, congratulations for completing the quest and clearing the domain adventurer. ")
    print("I am you, in another world, the creator of this domain and the first one who was able to complete and fail it.")
    print("It is my honor and duty to guide my self in this adventure. This is a gentle reminder to be unshakable and trust yourself,")
    print("because at the end of the day, the only person who truly has your back is you!")
    print("")
    print("Reward: You had doubts, but you went for it anyway. There was fear, but it didn't stop you. You knew it could fail, but you still did It.")
    print("You just acquired the treasure of all treasure, the art of trying.")

def playerName():
    playerInput = input("Please enter your name to start the game:  ")
    gameStart(playerInput)

def gameStart(player):
    print("")
    print(" WELCOME ADVENTURER...")
    print(" ")
    print("1. 'Where am I?'               2. 'No no no no. I need to go back Im too scared for this!!'")
    interact = input(player + ": ")
    if interact == "1":
        print("")
        print("You accidentally fall into portal while travelling...")
        print("You need to find the treasure chest and escape to clear this domain.")
        print("Do you wish to continue? Once you accept this quest, there is no turning back.")
        print("Note: The treasure chest will serve as your reward after you clear the game.")
    elif interact == "2":
        print("Game over. Sometimes, you just need to show up, even if you are scared...")
        exit()
    else:
        print("Invalid input. Please run the program again.")
        exit()

    print("")
    print("1. 'Treasure chest?!?! Hell yeahh let's conquer this domain!'  2. 'There is no need for me to complete this little game. I'm going back.'")
    interact1 = input(player + ": ")
    if interact1 == "1":
        print("")
        print("Warning: There is a server boss in this domain. Gather all of your luck and try to avoid him.")
        print("Warning: You can't defeat him...")
        print("")
    elif interact1 == "2":
        print("Game over. Failed to conquer this domain.")
        print("Terminating the portal...")
        exit()
    else:
        print("Invalid input. Please run the program again.")
        exit()

    print("Current location: Starting room.")
    print("Instruction: Guess the password of the door to proceed to next room.")
    print("")
    print("1. Guess the password  2. Surrender")
    interact2 = input(player + ": ")
    if interact2 == "1":
        guessThePassword()
    elif interact2 == "2":
        gameOver()
    else:
        print("Invalid input. Please run the program again.")

playerName()


