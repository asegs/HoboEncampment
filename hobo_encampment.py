import random
from datetime import date
header = "    __  __ ____   ____   ____     ______ _   __ ______ ___     __  ___ ____   __  ___ ______ _   __ ______\n   / / / // __ \ / __ ) / __ \   / ____// | / // ____//   |   /  |/  // __ \ /  |/  // ____// | / //_  __/\n  / /_/ // / / // __  |/ / / /  / __/  /  |/ // /    / /| |  / /|_/ // /_/ // /|_/ // __/  /  |/ /  / /   \n / __  // /_/ // /_/ // /_/ /  / /___ / /|  // /___ / ___ | / /  / // ____// /  / // /___ / /|  /  / /    \n/_/ /_/ \____//_____/ \____/  /_____//_/ |_/ \____//_/  |_|/_/  /_//_/    /_/  /_//_____//_/ |_/  /_/     "
path_levels = [".","x","*","@","X"]
house_levels = ["t","l","h","s","H"]
undeveloped_levels = ["%","&","#"]
paths = ["X","@","*","x",".","%","&","#"]
improvable_paths = ["@","*","x",".","%","&","#"]
fire_levels = ["f","F","B"]
garden_levels = ["g","n","N"]
farm_levels = ["r","R","C","P"]
quarry_levels = ["q","Q","S"]
metalworks_levels = ["m","M","U"]
upgradeable = [".","x","*","@","t","l","h","s","f","F","g","n","r","R","C","q","Q","m","M"]
map_width = 100
map_height = 29
grid = [["a" for i in range(map_width)] for j in range(map_height)]
help_string = "You are represented by the letter G.  Your goal is to survive.\nMove around this map with WASD, being careful not to run out of water and food.\nPlant a garden or make a farm for food, and drink from streams for water.\nUse b to build structures, x to destroy them, and i to interact with them.  Use u to perform upgrades.\nOnce you reach the road and have appealing housing, workers will come to live with you.\nBuild fires by houses to achieve this, and connect to level 3+ paths.\nThey can only come on level 3 and above paths, and you will need these to access stored materials.\nEnter c to save, and h to see this menu again.\n\n\n"

player_row = -1
player_col = -1
player_pos = " "
stats = {"Status":"Hello.","Standing on":" ","Health":10,"Water":100,"Food":100,"Turns without sleep":0,"Logs":0,"Stone":0,"Metal":0,"Stored logs":0,"Stored stone":0,"Stored metal":0,"House space":0,"Appeal":0,"Total people":0,"Unassigned people":0,"People logging":0,"People mining":0,"People metalworking":0,"People clearing":0,"Logs per turn":0,"Stone per turn":0,"Metal per turn":0,"Improvements per turn":0,"People's happiness":0,"Quarries sum level":0,"Metalworks sum level":0,"Road unlocked":False,"Unfinished":[]}
"""
upgrades array format is wood, stone, metal
"""
upgrades = {"Path":[[2,0,0],[5,2,0],[5,3,0],[10,5,1]],"House":[[10,0,0],[10,5,0],[20,10,5],[50,25,20]],"Fire":[[3,1,0],[5,3,1]],"Garden":[[10,0,0],[10,5,0]],"Farm":[[15,0,0],[20,5,0],[25,10,3]],"Quarry":[[100,20,0],[250,50,10]],"Metalworks":[[250,100,10],[500,250,50]]}
save_name = "default"

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
        if count<=1 and grid[row][col]!=" ":
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
        if stats["Turns without sleep"]>500:
            choice = random.randint(0,3)
            if choice == 3:
                direction = "a"
            elif choice == 2:
                direction = "s"
            elif choice == 1:
                direction = "w"
            else:
                direction = "d"
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
        if new_pos == " " or new_col<0 or new_row<0 or new_row>map_height or new_col>map_width or stats["Logs"]>3 or stats["Stone"]>3 or stats["Metal"]>3:
            stats["Status"] = "You are either overencumbered or trying to leave the map."
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
        stats["Status"] = "Out of bounds!"
        return grid
    

def regrow(percent = 0.001):
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
    global stats
    if player_pos not in path_levels:
        stats["Status"] = "You must be on a path to build."
        return grid
    choice = input("Enter the structure to build: log holder ('l'), house ('h'), bridge ('b'), campfire ('c'), garden ('g'),farm ('f'), quarry ('q'), metalworks ('m'), river ('r') or enter to close:")
    pos = input("Enter the movement direction to build in: 'WASD'")
    coords = select_new(pos)
    new_row = coords[0]
    new_col = coords[1]
    if new_row == player_row and new_col == player_col:
        stats["Status"] = "You're standing right there!"
        return grid
    try:
        tile = grid[new_row][new_col]
        if tile == " " and choice != "b" and choice != "r":
            stats["Status"] = "It sinks."
            return grid
        while tile in undeveloped_levels:
            stats["Turns without sleep"]+=paths.index(tile)
            tile = paths[paths.index(tile)-1]
        grid[new_row][new_col] = "."
    except:
        stats["Status"] = "You can't build over there."
        return grid
    if choice == "l":
        grid = build_params(1,"0",new_row,new_col)
    elif choice == "h":
        grid = build_params(5,"t",new_row,new_col)
    elif choice == "b":
        grid = build_params(3,".",new_row,new_col)
    elif choice == "c":
        grid = build_params(1,"f",new_row,new_col)
    elif choice == "g":
        grid = build_params(4,"g",new_row,new_col)
    elif choice == "f":
        grid = build_params(7,"r",new_row,new_col)
    elif choice == "q":
        grid = build_params(50,"q",new_row,new_col)
        stats["Quarries sum level"]+=1
    elif choice == "m":
        grid = build_params(125,"m",new_row,new_col)
        stats["Metalworks sum level"]+=1
    elif choice == "r":
        if if_borders(" ",new_row,new_col,True):
            grid[new_row][new_col] = " "
    return grid


def pull_from_unfinished(row,col):
    index = 0
    for todo in stats["Unfinished"]:
        if todo[1]==row and todo[2]==col:
            return index
        index+=1


def destroy():
    global player_row
    global player_col
    direction = input("What adjacent tile do you want to destroy? (WASD or ENTER to close):")
    coords = select_new(direction)
    new_row = coords[0]
    new_col = coords[1]
    if new_row == player_row and new_col == player_col:
        stats["Status"] = "You cannot destroy yourself.  That way, at least."
        return grid
    if grid[new_row][new_col]=="?":
        del stats["Unfinished"][pull_from_unfinished(new_row,new_col)]
    if grid[new_row][new_col] in quarry_levels:
        level = quarry_levels[quarry_levels.index(grid[new_row][new_col])+1]
        stats["Quarries sum level"]-=level
    if grid[new_row][new_col] in metalworks_levels:
        level = metalworks_levels[metalworks_levels.index(grid[new_row][new_col])+1]
        stats["Metalworks sum level"]-=level
    grid[new_row][new_col] = "."
    return grid


def take_stored(stored_string,string,number):
    if stats[stored_string]<number:
        number = stats[stored_string]
    stats[string]+=number
    stats[stored_string]-=number

def place_stored(stored_string,string,number):
    if stats[string]<number:
        number = stats[string]
    stats[string]-=number
    stats[stored_string]+=number

def interact():
    global player_row
    global player_col
    direction = input("What adjacent tile do you want to interact with? (WASD or ENTER to close):")
    coords = select_new(direction)
    new_row = coords[0]
    new_col = coords[1]
    if new_row == player_row and new_col == player_col:
        stats["Status"] = "You scratch your head."
        return grid
    if grid[new_row][new_col] == "?":
        unf_index = pull_from_unfinished(new_row,new_col)
        todo = stats["Unfinished"][unf_index]
        if len(todo)==4:
            if stats["Logs"]>=todo[3]:
                stats["Logs"]-=todo[3]
                grid[new_row][new_col] = todo[0]
                del stats["Unfinished"][unf_index]
            else:
                stats["Unfinished"][unf_index][3]-=stats["Logs"]
                stats["Logs"] = 0
            stats["Status"] = "You work on an old project."
            return grid
        if len(todo)==6:
            if stats["Logs"]>=todo[3] and stats["Stone"]>=todo[4] and stats["Metal"]>=todo[5]:
                stats["Logs"]-=todo[3]
                stats["Stone"]-=todo[4]
                stats["Metal"]-=todo[5]
                grid[new_row][new_col] = todo[0]
                del stats["Unfinished"][unf_index]
            else:
                if stats["Unfinished"][unf_index][3]>=stats["Logs"]:
                    stats["Unfinished"][unf_index][3]-=stats["Logs"]
                    stats["Logs"] = 0
                else:
                    stats["Logs"] -= stats["Unfinished"][unf_index][3]
                    stats["Unfinished"][unf_index][3]=0
                if stats["Unfinished"][unf_index][4]>=stats["Stone"]:
                    stats["Unfinished"][unf_index][4]-=stats["Stone"]
                    stats["Stone"] = 0
                else:
                    stats["Stone"] -= stats["Unfinished"][unf_index][4]
                    stats["Unfinished"][unf_index][4]=0
                if stats["Unfinished"][unf_index][5]>=stats["Metal"]:
                    stats["Unfinished"][unf_index][5]-=stats["Metal"]
                    stats["Metal"] = 0
                else:
                    stats["Metal"] -= stats["Unfinished"][unf_index][5]
                    stats["Unfinished"][unf_index][5]=0
            stats["Status"] = "You work on an old project."
            return grid
    if grid[new_row][new_col] in quarry_levels:
        stats["Stone"]+=quarry_levels.index(grid[new_row][new_col])+1
        if stats["Stone"]>3:
            stats["Stone"] = 3
    if grid[new_row][new_col] in metalworks_levels:
        stats["Metal"]+=metalworks_levels.index(grid[new_row][new_col])+1
        if stats["Metal"]>3:
            stats["Metal"] = 3
    if grid[new_row][new_col] == " ":
        stats["Water"] = 100
    if grid[new_row][new_col] in garden_levels or grid[new_row][new_col] in farm_levels:
        stats["Food"] = 100
    if grid[new_row][new_col] in house_levels:
        stats["Turns without sleep"] = 0
        stats["Health"] = 10
    if grid[new_row][new_col].isnumeric():
        count = int(grid[new_row][new_col])
        choice = input("Place logs ('p') or take logs ('t')?:")
        if choice == "p":
            if count+stats["Logs"]>=9:
                stats["Logs"]-=(9-count)
                count = 9
            else:
                count+=stats["Logs"]
                stats["Logs"] = 0
        else:
            stats["Logs"]+=count
            count = 0
        grid[new_row][new_col] = str(count)
    if grid[new_row][new_col] in path_levels:
        print("You can use level 3 and above paths to move materials mined by workers.")
        if path_levels.index(grid[new_row][new_col])>=2:
            while True:
                selection = input("Do you want to take materials ('t'), place materials ('p'), or press enter to exit:")
                if selection == "t":
                    choice  = input("Do you want to take logs ('l'), stone ('s'), metal ('m'), or press enter to return:")
                    number = input("How many do you want to take?:")
                    if number.isnumeric():
                        number = int(number)
                    else:
                        number = 0
                    if choice == "l":
                        take_stored("Stored logs","Logs",number)
                    elif choice == "s":
                        take_stored("Stored stone","Stone",number)
                    elif choice == "m":
                        take_stored("Stored metal","Metal",number)
                if selection == "p":
                    choice  = input("Do you want to place logs ('l'), stone ('s'), metal ('m'), or press enter to return:")
                    number = input("How many do you want to place?:")
                    if number.isnumeric():
                        number = int(number)
                    else:
                        number = 0
                    if choice == "l":
                        place_stored("Stored logs","Logs",number)
                    elif choice == "s":
                        place_stored("Stored stone","Stone",number)
                    elif choice == "m":
                        place_stored("Stored metal","Metal",number)
                else:
                    break
    return grid


def apply_costs(chart,index):
    row = chart[index]
    if stats["Logs"]>=row[0] and stats["Stone"]>=row[1] and stats["Metal"]>=row[2]:
        stats["Logs"]-=row[0]
        stats["Stone"]-=row[1]
        stats["Metal"]-=row[2]
        return True
    else:
        return False


def path_3_check(row,col):
    valid = False
    for i in range(2,len(path_levels)):
        valid = valid or if_borders(path_levels[i],row,col)
    for i in range(0,len(house_levels)):
        valid = valid or if_borders(house_levels[i],row,col)
    return valid


def upgrade_handler(string,levels,letter,new_row,new_col):
    global grid
    chart = upgrades[string]
    index = levels.index(letter)
    result = apply_costs(chart,index)
    if result==True:
        if letter in quarry_levels:
            stats["Quarries sum level"]+=1
        if letter in metalworks_levels:
            stats["Metalworks sum level"]+=1
        grid[new_row][new_col] = levels[levels.index(letter)+1]
    else:
        cost_arr = chart[index]
        logs = 0
        stone = 0
        metal = 0
        if cost_arr[0]>stats["Logs"]:
            logs = cost_arr[0]-stats["Logs"]
            stats["Logs"] = 0
        else:
            stats["Logs"]-=cost_arr[0]
        if cost_arr[1]>stats["Stone"]:
            stone = cost_arr[1]-stats["Stone"]
            stats["Stone"] = 0
        else:
            stats["Stone"]-=cost_arr[1]
        if cost_arr[2]>stats["Metal"]:
            metal = cost_arr[2]-stats["Metal"]
            stats["Metal"] = 0
        else:
            stats["Metal"]-=cost_arr[2]
        grid[new_row][new_col] = "?"
        todo = [levels[levels.index(letter)+1],new_row,new_col,logs,stone,metal]
        stats["Unfinished"].append(todo)
    return grid


def upgrade():
    global player_row
    global player_col
    global grid
    direction = input("What adjacent tile do you want to upgrade? (WASD or ENTER to close):")
    coords = select_new(direction)
    new_row = coords[0]
    new_col = coords[1]
    if (new_row == player_row and new_col == player_col) or grid[new_row][new_col] == " ":
        stats["Status"] = "That's either water or yourself.  Which are both perfect the way they are."
        return grid
    if grid[new_row][new_col] not in upgradeable:
        stats["Status"] = "You can't upgrade that."
        return grid
    letter = grid[new_row][new_col]
    if letter in path_levels:
        chart = upgrades["Path"]
        index = path_levels.index(letter)
        if index==0:
            return upgrade_handler("Path",path_levels,letter,new_row,new_col)
        elif path_3_check(new_row,new_col):
            if new_row>=map_height-1:
                    stats["Road unlocked"] = True
            return upgrade_handler("Path",path_levels,letter,new_row,new_col)
                
        return grid
    elif letter in house_levels:
        return upgrade_handler("House",house_levels,letter,new_row,new_col)
    elif letter in fire_levels:
        return upgrade_handler("Fire",fire_levels,letter,new_row,new_col)
    elif letter in garden_levels:
        return upgrade_handler("Garden",garden_levels,letter,new_row,new_col)
    elif letter in farm_levels:
        return upgrade_handler("Farm",farm_levels,letter,new_row,new_col)
    elif letter in quarry_levels:
        return upgrade_handler("Quarry",quarry_levels,letter,new_row,new_col)
    elif letter in metalworks_levels:
        return upgrade_handler("Metalworks",metalworks_levels,letter,new_row,new_col)
    return grid
    

def appeal_calc():
    house_space = 0
    appeal = 0
    for row in range(0,map_height):
        for col in range(0,map_width):
            if grid[row][col] in house_levels:
                house_size = house_levels.index(grid[row][col])+1
                for i in range(0,len(fire_levels)):
                    count = count_borders(fire_levels[i],row,col,True)
                    appeal+=(count*(i+1))
                appeal = appeal*house_size
                house_space+=house_size
    if not stats["Road unlocked"]:
        appeal = 0
    house_space-=stats["Total people"]
    return [house_space,appeal]

def happiness_calc():
    happiness = 0
    for row in range(0,map_height):
        for col in range(0,map_width):
            if grid[row][col] in farm_levels:
                happiness += 3*(farm_levels.index(grid[row][col])+1)
            if grid[row][col] in garden_levels:
                happiness += 2*(garden_levels.index(grid[row][col])+1)        
    return happiness/(stats["Total people"]+1)

def bring_people():
    if stats["House space"]>0 and stats["Appeal"]>0:
        if stats["Appeal"]*0.01>random.random():
            stats["Total people"]+=1
            stats["Unassigned people"]+=1


def assign_handler(string,number,code = 1):
    if code!=1:
        if number>stats[string]:
            number = stats[string]
    stats["Unassigned people"]-=(number*code)
    stats["People logging"]+=(number*code)
    

def assign_people():
    while True:
        choice = input("To assign to a category, enter ('a').  To remove from a category, enter ('r').  If you are satisfied, just press enter:")
        if choice == "a":
            category = input("Assign them to: logging ('l'), quarrying ('q'), metalworking ('m'), forest improvements ('i'), or press enter to return:")
            number = input("How many people will you assign?:")
            if number.isnumeric():
                number = int(number)
            else:
                number = 0
            if number>stats["Unassigned people"]:
                number = stats["Unassigned people"]
            if category == "l":
                assign_handler("People logging",number)
            elif category == "q":
                assign_handler("People mining",number)
            elif category == "m":
                assign_handler("People metalworking",number)
            elif category == "i":
                assign_handler("People clearing",number)
        elif choice == "r":
            category = input("Remove from: logging ('l'), quarrying ('q'), metalworking ('m'), forest improvements ('i'), or press enter to return:")
            number = input("How many people will you remove?:")
            if number.isnumeric():
                number = int(number)
            else:
                number = 0
            if category == "l":
                assign_handler("People logging",number,-1)
            if category == "q":
                assign_handler("People mining",number,-1)
            if category == "m":
                assign_handler("People metalworking",number,-1)
            if category == "i":
                assign_handler("People clearing",number,-1)
        else:
            break


def men_at_work(turns):
    clearers = stats["People clearing"]
    stats["Improvements per turn"] = int(stats["People's happiness"]*0.1*clearers)
    for i in range(0, stats["Improvements per turn"]*turns):
        tiles = map_height*map_width-1
        counter = 0
        while True:
            place = random.randint(0,tiles)
            row = int(place/map_width)
            col = place-row*map_width
            if grid[row][col] in improvable_paths:
                grid[row][col] = paths[paths.index(grid[row][col])-1]
                break
            counter+=1
            if counter>20:
                break
    loggers = stats["People logging"]
    stats["Logs per turn"] = int(stats["People's happiness"]*0.2*loggers)
    stats["Stored logs"]+=(turns*stats["Logs per turn"])
    miners = stats["People mining"]
    stats["Stone per turn"] = int(stats["People's happiness"]*0.1*miners*stats["Quarries sum level"])
    stats["Stored stone"]+=(turns*stats["Stone per turn"])
    metalworkers = stats["People metalworking"]
    stats["Metal per turn"] = int(stats["People's happiness"]*0.1*miners*stats["Metalworks sum level"])
    stats["Stored metal"]+=(turns*stats["Metal per turn"])
    

def status_gen():
    global player_pos
    if player_pos=="#":
        stats["Status"] = "You stand in thick vegetation."
    elif player_pos=="&":
        stats["Status"] = "You stand in waist high vegetation."
    elif player_pos=="%":
        stats["Status"] = "You stand in knee high grass."
    elif player_pos==".":
        stats["Status"] = "You stand on a rocky path."
    elif player_pos=="x":
        stats["Status"] = "You stand on a dirt path."
    elif player_pos=="*":
        stats["Status"] = "You stand on a much trodden path."
    elif player_pos=="@":
        stats["Status"] = "You stand on a well-maintained trail."
    elif player_pos=="X":
        stats["Status"] = "You stand on a paved road."
    if player_pos in undeveloped_levels:
        if random.random()<0.05:
            stats["Status"] = "You twist your ankle."
            stats["Health"]-=1
        if random.random()<0.08:
            stats["Status"] = "You find a huge bush of delicious strawberries."
            stats["Food"] = 100


def save():
    string = ""
    for row in range(0,map_height):
        for col in range(0,map_width):
            string+=grid[row][col]
        string+="\n"
    string+="-----"
    for key in stats:
        string+=str(stats[key])+"~"
    file = open(save_name+".txt","w")
    file.write(string)
    file.close()


def list_string_to_2d(string):
    lst = []
    string = string[1:len(string)-1]
    entries = string.split("],[")
    for i in range(0,len(entries)-1):
        entries[i] = entries[i].replace("]","")
        entries[i] = entries[i].replace("[","")
        entries[i] = entries[i].replace("'","")
        entries[i] = entries[i].replace(" ","")
        row = entries[i].split(",")
        lst.append(row)
    return lst


def find_player():
    for row in range(0,map_height):
        for col in range(0,map_width):
            if grid[row][col]=="G":
                return [row,col]


def split(word): 
    return [char for char in word]


def load(save_name):
    global map_height
    global map_width
    global grid
    global stats
    global player_row
    global player_col
    global player_pos
    grid = []
    string = ""
    file = open(save_name+".txt","r")
    for line in file:
        string+=line
    two_parts = string.split("-----")
    map_string = two_parts[0]
    stats_string = two_parts[1]
    rows = map_string.split("\n")
    map_height = len(rows)-1
    map_width = len(rows[0])
    for i in range(0,map_height):
        row = split(rows[i])
        grid.append(row)
    stats_rows = stats_string.split("~")
    counter = 0
    for key in stats:
        if stats_rows[counter].isnumeric():
            if len(stats_rows[counter].split("."))>1:
                stats[key] = float(stats_rows[counter])
            else:
                stats[key] = int(stats_rows[counter])
        elif stats_rows[counter] == "True":
            stats[key] = True
        elif stats_rows[counter] == "False":
            stats[key] = False
        elif "[" in stats_rows[counter]:
            stats[key] = list_string_to_2d(stats_rows[counter])
        else:
            stats[key] = stats_rows[counter]
        counter+=1
    player_coords = find_player()
    player_row = player_coords[0]
    player_col = player_coords[1]
    player_pos = stats["Standing on"]

def handler(choice):
    global grid
    if choice == "a" or choice == "w" or choice == "s" or choice == "d":
        grid = move_player(choice)
    elif choice == "b":
        grid = build()
    elif choice == "x":
        grid = destroy()
    elif choice == "i":
        grid = interact()
    elif choice == "u":
        grid = upgrade()
    elif choice == "p":
        assign_people()
    elif choice == "h":
        print(help_string)
        input("Press enter when done:")
    elif choice == "c":
        save()
    return grid

new_game = input("Do you want to start a new game ('s') or load an old one? ('l'):")
if new_game == "l":
    while True:
        save_name = input("Enter the filename, without .txt:")
        try:
            load(save_name)
            break
        except:
            choice = input("This is not a valid save. Type 'n' to make a new save, or enter to try again.")
            if choice=="n":
                new_game = "s"
                break
if new_game!="l":
    save_name = input("What will the save name be?:")
    if save_name.strip()=="":
        save_name = str(date.today())
    print(help_string)
    choice = input("You are about to generate a random map based on some presets.  Do you want normal ('n'), thick forest ('f'), thin forest ('t'), islands ('i'), or swamp ('s')?:")
    spawns = 0
    spread = 0
    cycles = 0
    tolerance = 0
    ruggedness = 0


    if choice == "f":
        spawns = 1
        spread = 0.5
        cycles = 100
        tolerance = 5
        ruggedness = 2
    if choice == "t":
        spawns = 2
        spread = 0.5
        cycles = 100
        tolerance = 5
        ruggedness = 0.75
    if choice == "i":
        spawns = 5
        spread = 0.5
        cycles = 100
        tolerance = 4
        ruggedness = 1
    if choice == "s":
        spawns = 5
        spread = 0.5
        cycles = 100
        tolerance = 4
        ruggedness = 0.25
    else:
        spawns = 3
        spread = 0.5
        cycles = 100
        tolerance = 5
        ruggedness = 1.5
    grid = draw_streams(spawns,spread,1)
    grid = erode(cycles,tolerance)
    grid = draw_land(ruggedness)
    place_player()
    status_gen()
    appeal_arr = appeal_calc()
    stats["House space"] = appeal_arr[0]
    stats["Appeal"] = appeal_arr[1]
    stats["Standing on"] = player_pos
    stats["People's happiness"] = happiness_calc()


road = draw_road()
save()
print(header)
print_board()
print(road)
turns = stats["Turns without sleep"]
while True:
    bring_people()
    choice = input("Make your move:")
    orig_status = stats["Status"]
    grid = handler(choice)
    handler_status = stats["Status"]
    stats["Standing on"] = player_pos
    for i in range(0,100):
        print()
    turns_passed = stats["Turns without sleep"]-turns
    if turns_passed<0:
        turns_passed = 0
    stats["Water"] -= int(turns_passed/2)
    stats["Food"] -=int(turns_passed/5)
    if stats["Water"]<0:
        orig_status = 0
        handler_status = "Dying of thirst!"
        stats["Health"]-=1
    if stats["Food"]<0:
        orig_status = 0
        handler_status = "Dying of starvation!"
        stats["Health"]-=0.5
    if stats["Turns without sleep"]>750:
        stats["Turns without sleep"] = 0
        stats["Logs"] = 0
        stats["Stone"] = 0
        stats["Metal"] = 0
        grid[player_row][player_col] = player_pos
        place_player()
    grid = regrow(0.00033*turns_passed)
    turns = stats["Turns without sleep"]
    appeal_arr = appeal_calc()
    stats["House space"] = appeal_arr[0]
    stats["Appeal"] = appeal_arr[1]
    stats["People's happiness"] = happiness_calc()
    status_gen()
    if orig_status!=handler_status:
        stats["Status"] = handler_status
    men_at_work(turns_passed)
    if stats["Health"]<0:
        exit()
    print(header)
    print_board()
    print(road)
"""

"""
