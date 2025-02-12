import sys
import os
import random
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
from Maps import maps, rooms
from Terminal import showCursor, hideCursor, typewrite

colorama_init()

FASTER = 0.001
FAST = 0.01
NORMAL = 0.03     #TODO Make Puzzles and Ghost
SLOW = 0.05
STARTING_ROOM = 5

global currRoom
currRoom = 5

def displayMap():
    for i in range(len(rooms[currRoom]["map"])):
        if i == 0 or i == len(rooms[currRoom]["map"])-1:
            print(f'{Fore.LIGHTYELLOW_EX}' + ('_'.join(rooms[currRoom]["map"][i])) + f'{Style.RESET_ALL}')
        else:
            print(f'{Fore.LIGHTYELLOW_EX}' + ' '.join(rooms[currRoom]["map"][i]) + f'{Style.RESET_ALL}')
    print()

def move(_currRoom: int):
    newRoom = _currRoom
    
    valid = False
    while not valid:
        typewrite("Where do you go? (N, S, E, W or back)", NORMAL)
        choice = input("> ").lower()
        match(choice):
            case "n":
                if newRoom > 2 and rooms[currRoom]["n"]:
                    newRoom -= 3 
                    valid = True
            case "s":
                if newRoom < 6 and rooms[currRoom]["s"]:
                    newRoom += 3
                    valid = True
            case "e":
                if newRoom != 2 and newRoom != 5 and newRoom != 8 and rooms[currRoom]["e"]:
                    newRoom += 1
                    valid = True
            case "w":
                if newRoom != 0 and newRoom != 3 and newRoom != 6 and rooms[currRoom]["w"]:
                    newRoom -= 1
                    valid = True
            case "back":
                break
        if not valid:
            typewrite("there is no door in that direction, Try another way...", FAST)
    return newRoom

def displayRoomMessage():
    hideCursor()
    typewrite((f'{Fore.YELLOW}' + rooms[currRoom]["description"] + f'{Style.RESET_ALL}'), NORMAL)
    showCursor()

def addItem(_room: int, _char: str):
    available = []
    for i in range(len(maps[currRoom])):
        for j in range(len(maps[currRoom][i])):
            if (i > 0 and i < len(maps[currRoom])-1) and (j > 0 and j < len(maps[currRoom][i])-1) and maps[_room][i][j] == ' ':
                available.append([i, j])

    chosen = random.choice(available)
    maps[_room][chosen[0]][chosen[1]] = _char

def removeItem(_room: int, _char: str):
    available = []
    for i in range(len(maps[currRoom])):
        for j in range(len(maps[currRoom][i])):
            if (i > 0 and i < len(maps[currRoom])-1) and (j > 0 and j < len(maps[currRoom][i])-1) and maps[_room][i][j] == _char:
                available.append([i, j])

    chosen = random.choice(available)
    maps[_room][chosen[0]][chosen[1]] = ' '
        
def generateDust():
    for room in range(len(maps)):
        for i in range(25):
            particles = ['.', ',', "'", "*", "`"]
            addItem(room, f'{Fore.LIGHTBLACK_EX}' + random.choice(particles) + f'{Fore.LIGHTYELLOW_EX}')

def fightMonster(a): 
    monsterHealth = random.randint(3, 8)
    stay = True
    while stay:
        print("Monster health: " + str(monsterHealth))
        print("Your Health: " + str(a))
        action = input("What do you do? R: Run, F: Roll -->  ").lower()
        if action == 'f':
            ghostRoll = random.randint(1, 6)
            humanRoll = random.randint(1, 6)
            if humanRoll >= ghostRoll:
                print('You hit the ghost for ' + str(humanRoll - ghostRoll) + ' Health')
                monsterHealth -= (humanRoll - ghostRoll)
            else:
                print('You were hit by the ghost for ' + str(humanRoll - ghostRoll) + ' Health')
                a -= (ghostRoll - humanRoll)
        elif action == 'r':
            ghostRoll = random.randint(1, 6)
            print('Monster hits.')
            print('Your HP ' + str(a))
            stay = False
        else:
            print("Error - press correct keys")
            print("Monster Hits")
            ghostRoll = random.randint(1, 6)
            a -= ghostRoll
        if monsterHealth <= 0:
            print("Monster lost")
            wounds = random.randint(1, 3)
            a += wounds
            print(a)
            stay = False
        elif a <= 0:
            print("You have been defeated")
            print("Game Over")
            quit()
    return a

def inspect():
    items = []
    for item in rooms[currRoom]["Items"]:
            items.append(item)
    
    if(len(items) == 0):
        typewrite("You search the room but find nothing")
    elif(len(items) == 1):
        typewrite("You found " + str(len(items)) + " Item!", SLOW)
    else:
        typewrite("You found " + str(len(items)) + " Items!", SLOW)

    for i in range(len(items)):
        typewrite("* " + items[i], SLOW)
        typewrite("1|---> Put it back", NORMAL)
        typewrite("2|---> Keep the item", NORMAL)

        choice = int(input("> "))
        match(choice):
            case 1:
                return
            case 2:
                inventory.append(items[i])
                rooms[currRoom]["Items"].remove(items[i])
                removeItem(currRoom, "!")
    displayMap()

def getInventory():
    global inventory
    for i in range(len(inventory)):
        typewrite(f"[{i+1}] {inventory[i]}", FAST)

def moveGhost():
    rand = random.randint(0, 8)
    while rand == 5:
        rand = random.randint(0, 8)

    global ghostRoom
    ghostRoom = rand

def menu():
    global currRoom
    
    hideCursor()
    typewrite(f"1|---> {Fore.WHITE}Move{Style.RESET_ALL}", FASTER)

    if(rooms[currRoom]["inspect"]):
        typewrite(f"2|---> {Fore.LIGHTYELLOW_EX}Inspect{Style.RESET_ALL}", FASTER)
    else:
        typewrite(f"2|---> {Fore.BLACK}Inspect{Style.RESET_ALL}", FASTER)

    typewrite(f"3|---> {Fore.WHITE}Quit{Style.RESET_ALL}", FASTER)
    showCursor()

    choice = input("> ")

    match(choice):
    case "1":
        currRoom = move(currRoom)
        return
    case "2":
        inspect()
    case "3":
        getInventory()
    case "4":
        sys.exit()
 
def init():
    global currRoom, ghostRoom
    currRoom = STARTING_ROOM
    ghostRoom = 0
    
    generateDust()
    for i in range(len(rooms)):
        for _ in rooms[i]["Items"]:
            addItem(i, f"{Fore.LIGHTRED_EX}!{Fore.LIGHTYELLOW_EX}")
    

# Main program
global ghostRoom
ghostRoom = 0

init()
quitGame = False
while not quitGame:
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Room " + str(currRoom))
    displayMap()
    displayRoomMessage()
    menu()
