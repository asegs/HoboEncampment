##from dataclasses import dataclass
import random
from os import system
header = "    __  __ ____   ____   ____     ______ _   __ ______ ___     __  ___ ____   __  ___ ______ _   __ ______\n   / / / // __ \ / __ ) / __ \   / ____// | / // ____//   |   /  |/  // __ \ /  |/  // ____// | / //_  __/\n  / /_/ // / / // __  |/ / / /  / __/  /  |/ // /    / /| |  / /|_/ // /_/ // /|_/ // __/  /  |/ /  / /   \n / __  // /_/ // /_/ // /_/ /  / /___ / /|  // /___ / ___ | / /  / // ____// /  / // /___ / /|  /  / /    \n/_/ /_/ \____//_____/ \____/  /_____//_/ |_/ \____//_/  |_|/_/  /_//_/    /_/  /_//_____//_/ |_/  /_/     "
path_levels = [".","x","*","@"]
house_levels = ["t","l","h","s","H"]
undeveloped_levels = ["%","&","#"]
paths = ["@","*","x",".","%","&","#"]
fire_levels = ["f","F","B"]
garden_levels = ["g","G","N"]
farm_levels = ["r","R","c","C","p","P"]
map_width = 100
map_height = 25
grid = [["a" for i in range(map_width)] for j in range(map_height)]

player_row = -1
player_col = -1
player_pos = " "
stats = {"Health":10,"Water":100,"Food":100,"Turns without sleep":0,"Logs":0,"Unfinished":[]}


def add_to_road(road,to_add=" "):
    for i in range(0,map_width):
        road+=to_add
    road+="\n"
    return road

def draw_road():
    road = ""
    road = add_to_road(road,"_")
    road = add_to_road(road)
    road = add_to_road(road)
    for i in range(0,map_width):
        if i%3==0:
            road+="="
        else:
            road+=" "
    road = add_to_road(road)
    road = add_to_road(road,"_")
    return road
        

def is_object(obj,row,col):
    try:
        if grid[row][col]==obj:
            return True
        else:
            return False
    except:
        return False

    
def if_borders(borders,row,col,diag=False):
    has_border = False
    if diag:
        has_border = is_object(borders,row-1,col-1) or is_object(borders,row+1,col-1) or is_object(borders,row-1,col+1) or is_object(borders,row+1,col+1)
    return has_border or is_object(borders,row-1,col) or is_object(borders,row,col-1) or is_object(borders,row,col+1) or is_object(borders,row+1,col)


def draw_streams(initial_waters = 3,water_percentage = 0.5,traces=1):
    tiles = map_width*map_height
    for i in range(0,initial_waters):
        place = random.randint(0,tiles-1)
        row = int(place/map_width)
        col = place - row*map_width
        grid[row][col] = " "
    for i in range(0,traces):
        for row in range(0,map_height):
            for col in range(0,map_width):
                if grid[row][col]=="a" and random.random()<water_percentage and if_borders(" ",row,col,True):
                    grid[row][col]=" "
        for row in range(map_height-1,-1,-1):
            for col in range(map_width-1,-1,-1):
                if grid[row][col]=="a" and random.random()<water_percentage and if_borders(" ",row,col,True):
                    grid[row][col]=" "
    return grid


def draw_land(ruggedness=1):
    ruggedness = ruggedness/2
    for row in range(0,map_height):
        for col in range(0,map_width):
            land = random.random()/ruggedness
            if grid[row][col]=="a":
                if land<0.333:
                    grid[row][col] = undeveloped_levels[2]
                elif land<0.666:
                    grid[row][col] = undeveloped_levels[1]
                else:
                    grid[row][col] = undeveloped_levels[0]
    return grid


def print_board():
    stats_printed = 0
    for row in range(0,map_height):
        string = ""
        for col in range(0,map_width):
            string +=grid[row][col]
        if stats_printed<len(stats):
            counter = 0
            for key in stats:
                if counter==stats_printed:
                    string+="   "+key+": "+str(stats[key])
                    stats_printed += 1
                    break
                counter+=1
            
        print(string)

def count_borders(obj,row,col,diag=True):
    count = 0
    for i in range(-1,2):
        try:
            if grid[row-1][col+i]==obj:
                count+=1
        except:
            count =count
        try:
            if grid[row+1][col+i]==obj:
                count+=1
        except:
            count=count
    try:
        if grid[row][col-1]==obj:
            count+=1
    except:
        count+=1
    try:
        if grid[row][col+1]==obj:
            count+=1
    except:
        count +=1
    return count
    

def erode(cycles=5,tolerance=6):
    for i in range(0,cycles):
        for row in range(0,map_height):
            for col in range(0,map_width):
                borders = count_borders(" ",row,col)
                if borders>tolerance:
                    grid[row][col] = " "
    return grid


def place_player():
    global player_row
    global player_col
    global player_pos
    tiles = map_height*map_width
    while True:
        placement = random.randint(0,tiles-1)
        row = int(placement/map_width)
        col = placement-row*map_width
        count = count_borders(" ",row,col)
        if count<=1:
            player_row = row
            player_col = col
            player_pos = grid[row][col]
            grid[row][col] = "G"
            break


def select_new(direction):
        global grid
        global player_row
        global player_col
        new_row = player_row
        new_col = player_col
        if direction == "a":
            new_row = player_row
            new_col = player_col-1
        if direction == "w":
            new_row = player_row-1
            new_col = player_col
        if direction == "s":
            new_row = player_row+1
            new_col = player_col
        if direction =="d":
            new_row = player_row
            new_col = player_col+1
        return [new_row,new_col]


def move_player(direction,distance=1):
    global player_row
    global player_col
    global grid
    global player_pos
    coords = select_new(direction)
    new_row = coords[0]
    new_col = coords[1]
    try:
        original_tile = player_pos
        new_pos = grid[new_row][new_col]
        if new_pos == " " or new_col<0 or new_row<0 or new_row>map_height or new_col>map_width or stats["Logs"]>3:
            return grid
        if player_pos in undeveloped_levels:
            stats["Logs"] += 1
            if stats["Logs"]>3:
                stats["Logs"] = 3
            place = undeveloped_levels.index(player_pos)
            if place == 0:
                player_pos = "."
            else:
                player_pos = undeveloped_levels[place-1]
        grid[player_row][player_col] = player_pos
        player_pos = grid[new_row][new_col]
        grid[new_row][new_col] = "G"
        player_row = new_row
        player_col = new_col
        stats["Turns without sleep"] += paths.index(original_tile)
        return grid
    except:
        print("Out of bounds")
        return grid
    

def regrow(percent = 0.003):
    global grid
    tiles = map_width*map_height
    chosen = []
    for i in range(0,int(percent*tiles)):
        chosen.append(int(random.random()*tiles-1))
    for i in chosen:
        row = int(i/map_width)
        col = i-row*map_width
        if grid[row][col] in paths and paths.index(grid[row][col])!=len(paths)-1:
            grid[row][col] = paths[paths.index(grid[row][col])+1]
    return grid


def build_params(cost,symbol,new_row,new_col):
    global grid
    if stats["Logs"]>=cost:
        stats["Logs"]-=cost
        grid[new_row][new_col] = symbol
    else:
        todo = [symbol,new_row,new_col,cost-stats["Logs"]]
        stats["Unfinished"].append(todo)
        grid[new_row][new_col] = "?"
        stats["Logs"] = 0
    return grid
        
def build():
    global grid
    global player_pos
    global player_row
    global player_col
    if player_pos not in path_levels:
        return grid
    choice = input("Enter the structure to build: log holder ('l'), house ('h'), bridge ('b'), campfire ('c'), garden ('g'),farm ('f'), or enter to close:")
    pos = input("Enter the movement direction to build in: 'WASD'")
    coords = select_new(pos)
    new_row = coords[0]
    new_col = coords[1]
    if new_row == player_row and new_col == player_col:
        return grid
    try:
        tile = grid[new_row][new_col]
        if tile == " ":
            return grid
        while tile in undeveloped_levels:
            stats["Turns without sleep"]+=paths.index(tile)
            tile = paths[paths.index(tile)-1]
        grid[new_row][new_col] = "."
    except:
        return grid
    if choice == "l":
        grid = build_params(1,"0",new_row,new_col)
    elif choice == "h":
        grid = build_params(5,"t",new_row,new_col)
    elif choice == "b" and stats["Logs"]>2 and grid[new_row][new_col] == " ":
        stats["Logs"]-=3
        grid[new_row][new_col] = "."
    elif choice == "b" and grid[new_row][new_col] == " ":
        todo = [".",new_row,new_col,3-stats["Logs"]]
        stats["Unfinished"].append(todo)
        grid[new_row][new_col] = "?"
        stats["Logs"] = 0
    elif choice == "c":
        grid = build_params(1,"f",new_row,new_col)
    elif choice == "g":
        grid = build_params(4,"g",new_row,new_col)
    elif choice == "f":
        grid = build_params(7,"r",new_row,new_col)
    return grid


def pull_from_unfinished(row,col):
    index = 0
    for todo in stats["Unfinished"]:
        if todo[1]==row and todo[2]==col:
            return index
        index+=1


def improve_structure():
    global grid
    global player_pos
    global player_row
    global player_col

def destroy():
    global player_row
    global player_col
    direction = input("What adjacent tile do you want to destroy? (WASD or ENTER to close):")
    coords = select_new(direction)
    new_row = coords[0]
    new_col = coords[1]
    if new_row == player_row and new_col == player_col:
        return grid
    if grid[new_row][new_col]=="?":
        del stats["Unfinished"][pull_from_unfinished(new_row,new_col)]
    grid[new_row][new_col] = "."
    return grid


def handler(choice):
    if choice == "a" or choice == "w" or choice == "s" or choice == "d":
        grid = move_player(choice)
    if choice == "b":
        grid = build()
    if choice == "x":
        grid = destroy()
    return grid


road = draw_road()
grid = draw_streams(3,0.5,1)
grid = erode(100,5)
grid = draw_land(1.5)
place_player()
print(header)
print_board()
print(road)
while True:
    choice = input("Make your move:")
    grid = handler(choice)
    for i in range(0,100):
        print()
    grid = regrow()
    print(header)
    print_board()
    print(road)
"""
Interact with function
Destroy function
Path to road check, will take too long, only allow starting level 3 path from house or other level 3 path
Improve function
"""
