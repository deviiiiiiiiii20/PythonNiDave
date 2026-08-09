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
        print("Color choices: Red, Green, Black")
        color = input("Enter your choice: ")
        if color == "Green" or color == "green" or color == "GREEN":
            print("")
            print("Status: You have successfully acquired the treasure chest and cleared the domain. Congratulations!")
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
    print("________________________________________________________________________"
          "______________________________________________________________________________________"
          "__________________________")
    print("")
    print("System, ")
    print("First, congratulations for completing the quest and clearing the domain adventurer. ")
    print("I am you, in another world, the creator of this domain and the first one who was able to complete and fail it.")
    print("It is my honor and duty to guide my self in this adventure. This is a gentle reminder to be unshakable and trust yourself,")
    print("because at the end of the day, the only person who truly has your back is you!")
    print("")
    print("Reward: You had doubts, but you went for it anyway. There was fear, but it didn't stop you. You knew it could fail, but you still did It.")
    print("You just acquired the treasure of all treasure, the art of trying.")
    print("________________________________________________________________________"
          "______________________________________________________________________________________"
          "__________________________")

def playerName():
    playerInput = input("Please enter your name to start the game:  ")
    gameStart(playerInput)


def gameStart(player):
    print("")
    print("Direction: Put the number of your corresponding answer.")
    print(" WELCOME adventurer " + player + "...")
    print(" ")
    print("1. 'Where am I?'")
    print(" 2. 'No no no no. I need to go back Im too scadred for this!!' ")
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
        print("1. 'Who decided that?! I just need to find something to defeat him.'")
        print("2. 'Fine!! I'll test my luck and clear this domain!'")
        interact3 = input(player + ": ")
        if interact3 == "1":
            pickUp(player)
        elif interact3 == "2":
            didNotPickup(player)
        else:
            print("Invalid input. Please run the program again.")
            exit()

    elif interact1 == "2":
        print("Game over. Failed to conquer this domain.")
        print("Terminating the portal...")
        exit()
    else:
        print("Invalid input. Please run the program again.")
        exit()


def didNotPickup(player):
    print("")
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

def pickupChallenge1(player):
    print("________________________________________________________________________"
          "______________________________________________________________________________________"
          "__________________________")
    print("")
    print("You have successfully killed the monster. ")
    print("System notice: The monster dropped a paper with a password clue.")
    print("")
    print("Warning: Pick up the paper for the clue and leave this area.")
    print("Final warning: The room is shaking.")
    print("")
    print("Action 1: Pick up the paper.")
    print("Action 2: Guess the password.")
    interact8 = input(player + ": ")
    if interact8 == "1":
        print(" ")
        print("Dear Player, ")
        print("I am always with you, but you can never see me.")
        print("Every clock counts me, and every minute brings me closer.")
        print("Extra Tip: I am a number.")
        print(" ")
        while True:
            password = input("Enter the password: ")
            if password == "1":
                print(" ")
                print("Door Unlocked. The room is now collapsing, run and get out of here.")
                print("Status: Challenge 1 Completed. Proceeding to the next room.")
                print("________________________________________________________________________"
                      "______________________________________________________________________________________"
                      "__________________________")
                pickAskilll(player)
                break

    elif interact8 == "2":
        print("You failed to guess the password. The room collapsed and killed you.")
        gameOver()
    else:
        print("You failed to guess the password. The room collapsed and killed you.")
        gameOver()


def pickAskilll(player):
    print("________________________________________________________________________"
          "______________________________________________________________________________________"
          "__________________________")
    print("System notice: You found a vault containing a skills. ")
    print("Note: You can only pick 1")
    print("")
    print("1. 'A skill that can see through things?!! I'll this!")
    print("2. 'Woahhh, a skill that can change the element of my sword. I'll take this one.")
    print("3. 'A skills comes with a great responsibility, besides, having a skill does not challenge me.")
    while True:
        skill = input(player + ": ")
        if skill == "1":
            pickApath("Devil's Eye", player)
            break
        elif skill == "2":
            pickApath("Element sword manipulation", player)
            break
        elif skill == "3":
            nonSkill(player)
            break
        else:
            print("Invalid input. Try again.")

def pickApath (skill, player):
    print("________________________________________________________________________"
          "______________________________________________________________________________________"
          "__________________________")
    print("")
    print("Now that you have escaped.")
    print("Pick a path to continue your journey.")
    print("System notice: You acquired a new skill '" + skill + "'.")
    print("System notice: Skill in cooldown.")
    print("")
    print("1. Door 1")
    print("2. Door 2")
    while True:
        path = input(player + ": ")
        if path == "1":
            blackout(player, skill)
            break
        elif path == "2":
            brighroom(player, skill)
            break
        else:
            print("Invalid input. Try again.")

def blackout(player, skill):
    print("________________________________________________________________________"
          "______________________________________________________________________________________"
          "__________________________")
    print("Challenge 2: The dark room.")
    print(" ")
    print( ": wait... why is it so dark??")
    print(" ")
    print("You are now in a powerless room. Find the gas to power up the generator.")
    print("Attention: The gas cage has a password.")

    myLuckyNumber = "0000"
    maxAttempts = 3

    for attempt in range(1, maxAttempts + 1):
        guess = input("Enter the password: ")
        if guess == myLuckyNumber:
            print("")
            print("Password is correct. The room is now powered up.")
            print("Status: Challenge 2 Completed. Proceeding to the next area.")
            print("________________________________________________________________________"
                  "______________________________________________________________________________________"
                  "__________________________")
            waterSource(player, skill)
            break
        elif attempt == 1:
            print("")
            print("Clue:")
            print("I am the exact time when a new day begins.")
            print("Write me as four digits without the colon.")
            print("")

        if attempt >= maxAttempts:
            print("")
            print("Maximum attempts reached. You got trapped in the dark room, there is no way out...")
            print("Game over. You Died.")
            print("________________________________________________________________________"
                  "______________________________________________________________________________________"
                  "__________________________")
            break

def waterSource(player, skill):
    print("________________________________________________________________________"
          "______________________________________________________________________________________"
          "__________________________")
    print("Warning: The water level of your body is low. Find a water source.")
    print("")
    print("System notice: An ice golem is approaching.")
    print("Warning: You can't defeat it.")
    print("Tip: Use your acquired skill.")
    print("Do you want to use your skill? (yes/no)")
    golem = input(player + ": ")
    if golem == "yes" or golem == "YES" or golem == "Yes":
        if skill == "Devil's Eye":
            print("")
            print("System notice: Skill 'Devil's eye' was used.")
            print(" ")
            print(" Fire golem has been defeated. ")
            print("Adventurer " + player + "saw the fire golem's core and destroyed it")
            print("________________________________________________________________________"
                  "______________________________________________________________________________________"
                  "__________________________")
            print("Status: Your found a water source. Body water level is now normal.")
            pickupChallenge3(player, skill)
        elif skill == "Element sword manipulation":
            print("")
            print("System notice: Skill 'Element sword manipulation' was used.")
            print("")
            print(" Fire golem has been defeated. ")
            print("Adventurer " + player + " changed his sword into water sword to cancel out the fire golem.")
            print("________________________________________________________________________"
                  "______________________________________________________________________________________"
                  "__________________________")
            print("Status: Your found a water source. Body water level is now normal.")
            pickupChallenge3(player, skill)
    elif golem == "no" or golem == "NO" or golem == "No":
        print(" ")
        print("Do you want to run? ")
        golem2 = input(player + ": ")
        if golem2 == "yes" or golem == "YES" or golem == "Yes":
            pickApath(skill, player)
        elif golem2 == "no" or golem == "NO" or golem == "No":
            print("The fire golem killed you.")
            gameOver()
    else:
        print("Invalid input. The system took it as a no")
        gameOver()


def brighroom(player, skill):
    print("________________________________________________________________________"
          "______________________________________________________________________________________"
          "__________________________")
    print("Challenge 2: The bright room.")
    print(" ")
    print(": wait... why is it so bright??")
    print(" ")
    print("You are now in a bright room. Find the switch panel to dim the light.")
    print("Attention: The switch panel has a password.")

    brightroomkey = "0000"
    maxAttempts = 3

    for attempt in range(1, maxAttempts + 1):
        bright = input("Enter the password: ")
        if bright == brightroomkey:
            print("")
            print("Password is correct. The light is now dim.")
            print("Status: Challenge 2 Completed. Proceeding to the next area.")
            print("________________________________________________________________________"
                  "______________________________________________________________________________________"
                  "__________________________")
            pickupChallenge3(player, skill)
            break
        elif attempt == 1:
            print("")
            print("Clue:")
            print("The third is the oldest.")
            print("The last is the youngest.")
            print("They are numbered in order.")
            print("")

        if attempt >= maxAttempts:
            print("")
            print("Maximum attempts reached. The light destroyed your eyes, there is no way out...")
            print("Game over. You Died.")
            print("________________________________________________________________________"
                  "______________________________________________________________________________________"
                  "__________________________")
            break

def pickupChallenge3(player, skill):
    print("________________________________________________________________________"
          "______________________________________________________________________________________"
          "__________________________")
    print("Challenge 3: The doors of fate.")
    print("")
    print("Pick a door to decide your fate. This is the final challenge for you adventurer " + player + " best of luck!")
    print(" ")
    print("1. Door 1: Marahuyo")
    print("2. Door 2: Kaulayaw")
    print("3. Door 3")
    playerDoor = input("Enter the door number: ")
    if playerDoor == "1":
        playerDoor1(player, skill)
    elif playerDoor == "2":
        playerDoor2(player, skill)

def playerDoor2(player, skill):
    print("________________________________________________________________________"
          "______________________________________________________________________________________"
          "__________________________")
    print("Welcome to the door of Kaulayaw.")
    print(" ")
    print("System notice: Another adventurer found.")
    print("Do you wish to interact? (Yes or No)")
    userinteract = input(player + ": ")
    if userinteract== "yes" or userinteract == "YES" or userinteract == "Yes":
        print(" ")
        print(player + "Hi! my name is " + player + ". What is your name?")
        print("Dene: nice to meet you "+ player + ". My name is Dene. What brings you to this domain?")
        print(player+ ": I did not exactly brought my self here, but I am here to conquer this domain.")
        print("Dene: looks like we're after the same destination. ")
        print(player + ": Really?! then we should make a team.")
        print("Dene: I do agree, neither of us should face the server boss alone.")
        print(player + ": Lets go!")
        print(" ")
        print("Warning: The server boss is here.")
        print("Final Warning: You can't defeat him.")
        print("Dene: Hey "+ player + " let's fuse together so we can defeat him!")
        print("Do you wish to fuse? (Yes or No)")
        fuse = input(player + ": ")
        if fuse == "yes" or fuse == "YES" or fuse == "Yes":
            print("")
            print("Fusing interrupted. Answer the question to bypass the process.")
            print("I have no feet, yet I guide your way.")
            print("I hold no treasure, but I lead you to it.")
            print("What am I?")
            useranswer = input(player + ": ")
            if useranswer == "Map" or useranswer == "MAP" or useranswer == "map":
                print("System notice: Fused sucessfully.")
                print("System notice: Attributes reached max level.")
                print("New title obtained: The blessed one")
                print(" ")
                print("System: The server boss has been defeated.")
                print(" ")
                print(
                "Status: You have successfully acquired the treasure chest and cleared the domain. Congratulations!")
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
                print("Fusing failed. The server boss crushed you.")
                print("Status: The server shutdown, cannot teleport you...")
                print("Status: Team member has been killed, cannot revive you...")
                gameOver()
        elif fuse == "no" or fuse == "NO" or fuse == "no":
            print("Warning: You can't defeat the server boss without awakening skills.")
            print("Warning: You can't defeat the server boss without awakening skills.")
            print("Warning: You can't defeat the server boss without awakening skills.")
            print("")
            print("The server boss crushed you. ")
            print("Status: The server shutdown, cannot teleport you...")
            print("Status: Team member has been killed, cannot revive you...")
            gameOver()
        else:
            print("Invalid action. No more chances.")
            gameOver()
    elif userinteract == "no" or userinteract == "NO" or userinteract == "no":
        print("System unique skill: Vision")
        print("System: The boss crushed you in an instant after you ignored the adventurer.")
        print("Invalid action. No more chances.")
        print(" ")
        print("Warning: You can't defeat the server boss without awakening skills.")
        print("Warning: You can't defeat the server boss without awakening skills.")
        print("Warning: You can't defeat the server boss without awakening skills.")
        gameOver()
    else:
        print("Invalid action. No more chances.")
        gameOver()

def playerDoor1(player, skill):
    print("________________________________________________________________________"
          "______________________________________________________________________________________"
          "__________________________")
    print("Welcome to the door of Marahuyo.")
    print(" ")
    print("Warning: The server boss is here.")
    print("Warning: The server boss is here.")
    print("Warning: The server boss is here.")
    print(" ")
    print("System: Do you wish to use your skill and fight him? (yes/no)")
    playerdoor1choice = input(player + ": ")
    if playerdoor1choice == "yes" or playerdoor1choice == "YES" or playerdoor1choice == "Yes":
        if skill == "Devil's Eye":
            print("")
            print("System notice: Skill 'Devil's eye' was used.")
            print(" ")
            print("The server boss has been defeated. ")
            print("Adventurer " + player + "saw the server boss's core and destroyed it")
            print("________________________________________________________________________"
                  "______________________________________________________________________________________"
                  "__________________________")
            print("Status: You found a chest and cleard this.......")
            print("Warning: The server boss has revived.")
            print("Warning: The server boss has revived.")
            print("Warning: The server boss has revived.")

            print("System: Level requirement for awakening reached. Do you wish to awaken your special skill? (yes/no)"
                  " ")
            userskillchoice = input(player + ": ")
            if userskillchoice == "yes" or userskillchoice == "YES":
                print(" ")
                print("System: Awakening.. new title obtained.")
                print("New title: Conquerer")
                print("Status: Maximum stats reached")
                print(" ")
                print("The server boss has been defeated. ")
                print(" ")
                print(
                    "Status: You have successfully acquired the treasure chest and cleared the domain. Congratulations!")
                print("The system has a final note for you. Would you like to open it? (YES / NO) ")
                action = input("Action: ")
                if action == "YES" or action == "Yes" or action == "yes":
                    gameVictory()
                elif action == "NO" or action == "NO" or action == "no":
                    print("Domain successfully cleared. CONGRATS ADVENTURER.")
                else:
                    print("Invalid action")
                    exit()
            elif userskillchoice == "no" or userskillchoice == "NO" or userskillchoice == "no":
                print(" ")
                print("Warning: You can't defeat the server boss without awakening skills.")
                print("Warning: You can't defeat the server boss without awakening skills.")
                print("Warning: You can't defeat the server boss without awakening skills.")
                print("")
                print("The server boss crushed you. ")
                print("Status: The server shutdown, cannot teleport you...")
                gameOver()

        elif skill == "Element sword manipulation":
            print("")
            print("System notice: Skill 'Element sword manipulation' was used.")
            print("")
            print("The server boss has been defeated. ")
            print("Adventurer " + player + " enhanced the attributes of his sword to defeat the server boss.")
            print("________________________________________________________________________"
                  "______________________________________________________________________________________"
                  "__________________________")
            print("Status: You found a chest and cleard this.......")
            print("Warning: The server boss has revived.")
            print("Warning: The server boss has revived.")
            print("Warning: The server boss has revived.")
            print(" ")
            print("System: Level requirement for awakening reached. Do you wish to awaken your special skill? (yes/no)"
                  " ")
            userskillchoice = input(player + ": ")
            if userskillchoice == "yes" or userskillchoice == "YES":
                print(" ")
                print("System: Awakening.. new title obtained.")
                print("New title: Elemental master")
                print("Status: Maximum stats reached")
                print(" ")
                print("The server boss has been defeated. ")
                print(" ")
                print(
                    "Status: You have successfully acquired the treasure chest and cleared the domain. Congratulations!")
                print("The system has a final note for you. Would you like to open it? (YES / NO) ")
                action = input("Action: ")
                if action == "YES" or action == "Yes" or action == "yes":
                    gameVictory()
                elif action == "NO" or action == "NO" or action == "no":
                    print("Domain successfully cleared. CONGRATS ADVENTURER.")
                else:
                    print("Invalid action")
                    exit()
            elif userskillchoice == "no" or userskillchoice == "NO" or userskillchoice == "no":
                print(" ")
                print("Warning: You can't defeat the server boss without awakening skills.")
                print("Warning: You can't defeat the server boss without awakening skills.")
                print("Warning: You can't defeat the server boss without awakening skills.")
                print("")
                print("The server boss crushed you. ")
                print("Status: The server shutdown, cannot teleport you...")
                gameOver()

    elif playerdoor1choice == "no" or playerdoor1choice == "NO" or playerdoor1choice == "No":
        print(" ")
        print("Warning: You can't defeat the server boss without a skill.")
        print("Warning: You can't defeat the server boss without a skill.")
        print("Warning: You can't defeat the server boss without a skill.")
        print(" ")
        print("The system is teleporting you...")
        print("System: You can't die here.")
        pickupChallenge3(skill, player)
    else:
        print("Invalid input. The system took it as a no")
        gameOver()

def nonSkill(player):
    print("________________________________________________________________________"
          "______________________________________________________________________________________"
          "__________________________")

    print(player + ":I hope I won't regret my decision tho.")
    print(player + ":Oh wait. who's that?")
    print(" ")
    print("System notice: Another adventurer found.")
    print("Do you wish to interact? (Yes or No)")
    nonskilluser = input(player + ": ")
    if nonskilluser == "yes" or nonskilluser == "YES" or nonskilluser == "Yes":
        print(" ")
        print(player + "Hi! my name is " + player + ". What is your name?")
        print("Dene: nice to meet you "+ player + ". My name is Dene. What brings you to this domain?")
        print(player+ ": I did not exactly brought my self here, but I am here to conquer this domain.")
        print("Dene: looks like we're after the same destination. ")
        print(player + ": Really?! then we should make a team.")
        print("Dene: I am sosorry but I don't know if I can join you right now. ")
        print(player + ": Oh, is that so? ")
        print("Dene: But, if the destiny will allow it, I will definitely join you later!")

        print("")
        print("Dene: There is a portal there. You need to unlock it so that you can scape!")
        print("Warning: A monster is approaching.")
        print("System: Do you wish to fight this monster? (yes/no)")
        print("Tips: Fight the monster by answering riddles to unlock the portal.")
        fight = input(player + ": ")
        if fight == "yes" or fight == "YES" or fight == "Yes":
            print("________________________________________________________________________"
                  "______________________________________________________________________________________"
                  "__________________________")
            print("Direction: Find how many N are in these line of letters.")
            print("Warning: You only have 1 chance.")
            print("MMMMMMMMMMMMMMNMMMMMMNNMMMMMMMNN")
            number = input(player + ": ")
            if number == "5" or number == "five" or number == "FIVE" or number == "Five":
                print("Answer correct. Proceeding to next riddle.")
                print("________________________________________________________________________"
                      "______________________________________________________________________________________"
                      "__________________________")
                print(" ")
                print("I cannot speak, yet I open secrets.")
                print("Without me, many adventures come to an end.")
                print("What am I?")
                answer = input(player + ": ")
                if answer == "key" or answer == "Key" or answer== "KEY":
                    print(" ")
                    print("Quest complete: You killed the monster and unlocked the portal.")
                    print("Teleporting you..")
                    sure(player)
                else:
                    print("Quest failed. The monster killed you.")
                    gameOver()


    elif nonskilluser == "no" or nonskilluser == "NO" or nonskilluser == "no":
        print("")
        print("Monster approaching. Do you wish to fight? (yes or no)")
        skillwish = input(player + ": ")
        if skillwish == "yes" or skillwish == "YES" or skillwish == "Yes":
            print(" ")
            print("Warning: That is a server boss. You can't defeat him!")
            print("Status: The server boss killed you.")
            gameOver()
        elif skillwish == "no" or skillwish == "NO" or skillwish == "no":
            print(" ")
            print("Warning: That is a server boss. You can't defeat him!")
            print("System: You can't die here. Teleporting you...")
            nonSkill(player)
        else:
            print("Invalid input. The system took it as a no")
            print("System: You can't die here. Teleporting you...")
            nonSkill(player)

    else:
        print("Invalid input. The system took it as a no")
        print("Monster approaching. Do you wish to fight? (yes or no)")
        skillwish = input(player + ": ")
        if skillwish == "yes" or skillwish == "YES" or skillwish == "Yes":
            print(" ")
            print("Warning: That is a server boss. You can't defeat him!")
            print("Status: The server boss killed you.")
            gameOver()
        elif skillwish == "no" or skillwish == "NO" or skillwish == "no":
            print(" ")
            print("Warning: That is a server boss. You can't defeat him!")
            print("System: You can't die here. Teleporting you...")
            nonSkill(player)
        else:
            print("Invalid input. The system took it as a no")
            print("System: You can't die here. Teleporting you...")
            nonSkill(player)

def sure(player):
        print("________________________________________________________________________"
              "______________________________________________________________________________________"
              "__________________________")
        print("System notice: The portal is unstable. A strange light seeps through the cracks.")
        print(" ")
        print("Dene: " + player + "! Before you go through, take this.")
        print(player + ": What is it?")
        print("Dene: A fragment I found in this domain. I couldn't awaken it myself, but maybe you can.")
        print(" ")
        print("System notice: The fragment resonates with your resolve.")
        print("Attention: Answer this to awaken the fragment's power.")
        print("")
        print("I have cities, but no houses.")
        print("I have mountains, but no trees.")
        print("I have water, but no fish.")
        print("What am I?")
        fragmentAnswer = input(player + ": ")
        if fragmentAnswer == "map" or fragmentAnswer == "Map" or fragmentAnswer == "MAP":
            print(" ")
            print("System notice: Fragment awakened.")
            print("System notice: New skill obtained - 'Adventurer's Instinct'.")
            print("Dene: Looks like it chose you after all. Good luck out there, " + player + ".")
            print("________________________________________________________________________"
                  "______________________________________________________________________________________"
                  "__________________________")
            nonskillquest1(player)
        else:
            print(" ")
            print("System notice: The fragment rejected you. It shatters into dust.")
            print("Dene: ...I'm sorry, " + player + ". Without it, you won't survive what's ahead.")
            print("Status: The portal collapses on top of you.")
            gameOver()

def nonskillquest1(player):
    print("________________________________________________________________________"
          "______________________________________________________________________________________"
          "__________________________")
    print("")
    print("I am here because of the fragment... ")
    print("")
    print("Challenge x: The dark room.")
    print(" ")
    print(": wait... why is it so dark??")
    print(" ")
    print("You are now in a powerless room. Find the gas to power up the generator.")
    print("Attention: The gas cage has a password.")

    myLuckyNumber = "0000"
    maxAttempts = 3

    for attempt in range(1, maxAttempts + 1):
        guess = input("Enter the password: ")
        if guess == myLuckyNumber:
            print("")
            print("Password is correct. The room is now powered up.")
            print("Status: Challenge 2 Completed. Proceeding to the next area.")
            print("________________________________________________________________________"
                  "______________________________________________________________________________________"
                  "__________________________")
            nonskillquest2(player)
            break
        elif attempt == 1:
            print("")
            print("Clue:")
            print("I am the exact time when a new day begins.")
            print("Write me as four digits without the colon.")
            print("")

        if attempt >= maxAttempts:
            print("")
            print("Maximum attempts reached. You got trapped in the dark room, there is no way out...")
            print("Game over. You Died.")
            print("________________________________________________________________________"
                  "______________________________________________________________________________________"
                  "__________________________")
            break
def nonskillquest2(player):
    print("________________________________________________________________________"
          "______________________________________________________________________________________"
          "__________________________")
    print("________________________________________________________________________"
          "______________________________________________________________________________________"
          "__________________________")
    print("Welcome to Final quest. The air feels familiar here.")
    print(" ")
    print("???: " + player + "? Is that really you?")
    print(player + ": That voice... Dene?!")
    print(" ")
    print("Dene: I told you destiny would bring us together again, didn't I?")
    print(player + ": You actually came through. I can't believe it.")
    print("Dene: I've been tracking the server boss's signal since we parted. It's close. Very close.")
    print(" ")
    print("Warning: The server boss emerges from the shadows.")
    print("Warning: The server boss emerges from the shadows.")
    print("Warning: The server boss emerges from the shadows.")
    print(" ")
    print("Dene: This thing is stronger than before. Neither of us can take it alone.")
    print("Dene: " + player + ", do you still have your skill?")
    print("System: Do you wish to fuse with Dene to face the server boss? (yes/no)")
    fusechoice = input(player + ": ")
    if fusechoice == "yes" or fusechoice == "YES" or fusechoice == "Yes":
        print(" ")
        print("System notice: Fusion sequence initiated.")
        print("Attention: The fusion is unstable. Answer correctly to stabilize it.")
        print("")
        print("Two hearts, one purpose.")
        print("Alone we are strong, together we are unstoppable.")
        print("What bond do we share?")
        bondanswer = input(player + ": ")
        if bondanswer == "trust" or bondanswer == "Trust" or bondanswer == "TRUST":
            print(" ")
            print("System notice: Fusion stabilized.")
            print("System notice: '" + player + "' merged with Dene's power.")
            print("New title obtained: The Unbroken Bond")
            print(" ")
            print(player + " & Dene: Let's finish this - together!")
            print(" ")
            print("System: The server boss has been defeated.")
            print(" ")
            print("Status: You have successfully acquired the treasure chest and cleared the domain. Congratulations!")
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
            print(" ")
            print("System notice: Fusion failed. The bond wasn't strong enough - yet.")
            print("Dene: " + player + ", hold on!")
            print("Status: The server boss crushed you both.")
            print("Status: The server shutdown, cannot teleport you...")
            gameOver()
    elif fusechoice == "no" or fusechoice == "NO" or fusechoice == "no":
        print(" ")
        print("Dene: Then I'll hold him off. Go, " + player + "! Don't waste this chance!")
        print("Warning: You can't defeat the server boss alone.")
        print("Warning: You can't defeat the server boss alone.")
        print("Warning: You can't defeat the server boss alone.")
        print(" ")
        print("The server boss crushed you both.")
        print("Status: The server shutdown, cannot teleport you...")
        gameOver()
    else:
        print("Invalid action. No more chances.")
        gameOver()


def pickUp(player):
    print("")
    print("1. 'I'll start looking for a weapon'")
    print("2. 'Never mind I'll just clear this game only with my hands'")
    interact4 = input(player + ": ")
    if interact4 == "1":
        print(" ")
        print("You angered the server boss by picking up a sword.")
        print("This room will soon collapse hurry, take the door and leave this room!")
        print(" ")
        print("1. 'OK, so I just need to take that door and head to the next room.'")
        print("2. 'Angered? And how this room will collapse if it is built with the finest materials? I reject your order to move!'")
        print(" ")
        interact5 = input(player + ": ")
        if interact5 == "1":
            print(" ")
            print(player + ": Oh no! the door has a password. What should I do?!")
            print("System notice: Enemy approaching. Defeat the enemy before this room collapse.")
            print(" ")
            print("1. 'Even if I have this sword, there's no way that I can defeat that! I have to run!")
            print("2. 'I'm not so sure if this will works but, I'm giving my all, even my life!")
            interact6 = input(player + ": ")
            if interact6 == "1":
                print("")
                print("System notice: There's no way out")
                print("Status: Stamina running out. Continue to run? or try your luck and fight the monster? ")
                print("")
                print("1. 'This monster has so much aura, I can't defeat him. I'll just run and survive!'")
                print("2. 'Fine! I'm tired of running, at least I might die with honor.'")
                interact7 = input(player + ": ")
                if interact7 == "1":
                    print("")
                    print("Game over. The monster caught and killed you")
                elif interact7 == "2":
                    pickupChallenge1(player)
                else:
                    print("Invalid input. plyer " + player + " did not move.")
                    print("Game. The monster caught and killed you")
                    exit()
            elif interact6 == "2":
                pickupChallenge1(player)
            else:
                print("Invalid input. Please run the program again.")
                exit()

        elif interact5 == "2":
            print("Game over. A monster approached from above and killed you")
            exit()
        else:
            print("Invalid input. Please run the program again.")
            exit()
    if interact4 == "2":
        didNotPickup(player)

playerName()