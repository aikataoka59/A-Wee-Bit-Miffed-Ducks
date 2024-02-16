import math
import random
import sweeperlib

"""
You can change these values here:
WIN_WIDTH: window's width
WIN_HEIGHT: window's height
GRAVITATIONAL_ACCEL: a volume of gravity
FIRST_STAGE: text file's name of first stage
MAX_TARGET: max number of targets for random mode
MAX_OBSTACLE: max number of obstacles for random mode
"""
WIN_WIDTH = 1000
WIN_HEIGHT = 600
GRAVITATIONAL_ACCEL = 1
FIRST_STAGE = "stage1.txt"
MAX_TARGET = 3
MAX_OBSTACLE = 5

#This dictionary is called game dictionary
game = {
    "x": 60,
    "y": 80,
    "angle": 0,
    "force": 0,
    "x_drag":60,
    "y_drag":80,
    "x_velocity": 0,
    "y_velocity": 0,
    "flight": False,
    "stage_num": 1,
    "duck_num": 0,
    "win": False,
    "playing": False,
    "current_stage": FIRST_STAGE,
    "next_stage": "",
    "target": [],
    "obstacle": []
}

def initial_state():
    """
    Puts the duck back into its initial state:
    the duck is put back into the launch position,
    its speed, angle, force to zero, and its flight state to False.
    """
    game["x"] = game["x_drag"] = 60
    game["y"] = game["y_drag"] = 80
    game["angle"] = 0
    game["force"] = 0
    game["x_velocity"] = 0
    game["y_velocity"] = 0
    game["flight"] = False

def read_file(filename):
    """
    Read a text file of stage information and
    change variables of the game dictionary.
    Changes stage name, available number of ducks,
    stage number, next stage's name got from the file.
    Creates a dictionary of targets and obstacles, and
    it contains its x, y coordinate from the file.

    Filename should be given as its parameter
    Radius of targets and obstacles should be changed here.

    The text file should look like:
    stage_name stage1.txt
    duck_num 7
    stage_num 1
    next_stage stage2.txt
    target 800 100
    target 500 250
    obstacle 750 300
    obstacle 750 250
    """
    game["target"] = []
    game["obstacle"] = []
    with open(filename, "r", encoding='utf-8') as source:
        for line in source:
            elements = line.strip().split()
            if elements[0] == "target":
                x, y = int(elements[1]), int(elements[2])
                target = {"x": x, "y": y, "r": 40}
                game["target"].append(target)
            elif elements[0] == "obstacle":
                x, y = int(elements[1]), int(elements[2])
                obstacle = {"x": x, "y": y, "r": 20}
                game["obstacle"].append(obstacle)
            elif elements[0] == "duck_num":
                game["duck_num"] = int(elements[1])
            elif elements[0] == "next_stage":
                game["next_stage"] = str(elements[1])
            elif elements[0] == "stage_num":
                game["stage_num"] = int(elements[1])
            elif elements[0] == "stage_name":
                game["current_stage"] = elements[1]

def draw_object():
    """
    Draws all targets and obstacles written in the the game dictionary.
    """
    for target in game["target"]:
        x, y = target["x"], target["y"]
        sweeperlib.prepare_sprite("sling", x, y)
    for obstacle in game["obstacle"]:
        x, y = obstacle["x"], obstacle["y"]
        sweeperlib.prepare_sprite(" ", x, y)


def draw_menu():
    """
    This function handles interfaces and objects drawing in the main menu.
    """
    sweeperlib.clear_window()
    sweeperlib.draw_background()
    sweeperlib.begin_sprite_draw()
    sweeperlib.prepare_sprite("duck", 150, 150)
    sweeperlib.prepare_sprite("duck", 330, 250)
    sweeperlib.prepare_sprite("duck", 600, 300)
    sweeperlib.prepare_sprite("duck", 825, 225)
    sweeperlib.prepare_sprite("sling", 800, 100)
    sweeperlib.draw_sprites()
    sweeperlib.draw_text("A Wee Bit Miffed Ducks",90, 380,size=60)
    sweeperlib.draw_text("S: Start Game",325, 150,size=25)
    sweeperlib.draw_text("R: Random Stage Mode",325, 100,size=25)
    sweeperlib.draw_text("Q: Quit",325, 50,size=25)

def draw_result():
    """
    This function handles interfaces of the  result screen.
    It changes the shown texts depending on if users win or lose,
    if users clear all stage, and if users finish random mode.
    """
    sweeperlib.clear_window()
    sweeperlib.draw_background()
    sweeperlib.begin_sprite_draw()
    if game["win"]:
        if game["next_stage"] == "clear":
            sweeperlib.draw_text("Congraturation!",90, 380,size=60)
            sweeperlib.draw_text("You cleared all the stages!",90, 300,size=45)
        else:
            sweeperlib.draw_text("You won!",90, 380,size=60)
            sweeperlib.draw_text("N: Next Stage",625, 200,size=25)
    elif game["current_stage"]== "random.txt" and game["stage_num"]>1:
        sweeperlib.draw_text(
            "Your score: "
            +str(game["stage_num"])+
            " stages"
            ,90, 380,size=60)
    else:
        sweeperlib.draw_text("You lose...",90, 380,size=60)
    sweeperlib.draw_text("M: Main menu",625, 150,size=25)
    sweeperlib.draw_text("R: Restart",625, 100,size=25)
    sweeperlib.draw_text("Q: Quit",625, 50,size=25)


def draw_map():
    """
    This function handles interfaces and objects drawing in game stages.
    Shows the stage number and the number of remaining ducks.
    """
    sweeperlib.clear_window()
    sweeperlib.draw_background()
    sweeperlib.begin_sprite_draw()
    draw_object()
    sweeperlib.prepare_sprite("duck", game["x"], game["y"])
    sweeperlib.draw_sprites()
    if not game["flight"]:
        sweeperlib.draw_text("DRAG AND RELEASE!",20, 30, size=15)
    sweeperlib.draw_text(
        "Q: Quit  | "
        "R: Start from beginning |  "
        "M: Main menu",
        15, 560,
        size=20
    )
    sweeperlib.draw_text(
        "Stage No."
        +str(game["stage_num"])+
        "  Remaining Ducks:  "
        +str(game["duck_num"]),
        15, 505,
        size=25
    )

def keypress_menu(sym, mods):
    """
    This function handles keyboard input in a main menu.
    S: starts the normal mode
    R: starts the random stage mode
    Q: closes the window
    """
    key = sweeperlib.pyglet.window.key

    if sym == key.S:
        game["current_stage"] = FIRST_STAGE
        game["playing"]=True
        stage()
    if sym == key.R:
        read_file("random.txt")
        game["playing"]=True
        random_stage()
    if sym == key.Q:
        sweeperlib.close()

def keypress_map(sym, mods):
    """
    This function handles keyboard input in a game stage and a result screen.
    N: let users move to next stage if they complete previous one and if there's next one
    Q: closes the window
    R: puts game into initial status and restarts the game
    M: puts game into initial status and moves to main menu
    """
    key = sweeperlib.pyglet.window.key
    if game["win"] and sym == key.N and game["next_stage"] != "clear":
        game["current_stage"] = game["next_stage"]
        game["playing"] = True
        game["win"] = False
        initial_state()
        stage()
    if sym == key.Q:
        sweeperlib.close()
    if sym == key.R:
        initial_state()
        game["playing"] = True
        if game["current_stage"] == "random.txt":
            read_file("random.txt")
            random_stage()
        else:
            game["current_stage"] = FIRST_STAGE
            game["win"] = False
            stage()
    if sym == key.M:
        game["playing"]=False
        game["win"] = False
        initial_state()
        main_menu()

def handle_drag(x_mouse, y_mouse, x_change, y_change, mouse_button, modifiers):
    """
    This function is called when the mouse is moved while one of its buttons is pressed down.
    Records the x y coordinate of the mouse after dragging to the game dictionary.
    """
    if game["playing"] and not game["flight"]:
        game["x_drag"] += x_change
        game["y_drag"] += y_change

def handle_release(x_mouse, y_mouse, mouse_button, modifiers):
    """
    This function is called when the mouse's buttons is released.
    Calculates and set angle and force that users wants the duck to fly, and call launch function.
    """
    if game["playing"] and not game["flight"]:
        drag_direction_x = game["x_drag"] - game["x"]
        drag_direction_y = game["y_drag"] - game["y"]
        radian = math.atan2(-drag_direction_y, -drag_direction_x)
        drag_distance = calculate_distance(game["x_drag"], game["y_drag"], game["x"], game["y"])

        game["angle"] = radian
        game["force"] = drag_distance*(1/10)
        launch()

def calculate_distance(x_1,y_1,x_2,y_2):
    """
    Calculates the distance between two points and returns it.
    """
    return math.sqrt((x_1-x_2)**2+(y_1-y_2)**2)

def check_collision(object_1, object_2):
    """
    Calculates the distance between two objects and returns True
    if the objects hit each other, False if they do not.
    The objects'x,y coordinate should be a center of them.
    """
    result = False
    distance = calculate_distance(object_1['x'], object_1['y'], object_2['x'], object_2['y'])
    if distance <= (object_1['r']+object_2['r']):
        result = True
    return result

def launch():
    """
    Launches a duck and calculates its starting velocity.
    Stores x and y velocity components to the game dictionary.
    """
    if game["playing"]:
        game["flight"] = True
        game["x_velocity"] = float(game["force"]*math.cos(game["angle"]))
        game["y_velocity"] = float(game["force"]*math.sin(game["angle"]))

def flight(elapsed_time):
    """
    Updates duck's x and y coordinates based on corresponding velocity vectors.
    Stops ducks, put them into initial status, and reduce the num of remaining ducks
    if they hit by obstacles, or if they hit the bottom.
    Removes targets hit by duck from the game dictionary.
    Ends game if the number of remaining ducks is zero,
    or if all targets are destroyed.

    """
    if game["playing"]:
        if game["duck_num"]<1:
            gameover()
        else:
            if game["flight"]:
                game["x"] += game["x_velocity"]
                game["y"] += game["y_velocity"]
                game["y_velocity"] -= GRAVITATIONAL_ACCEL

            duck = {"x": game["x"]+20, "y": game["y"]+20, "r": 20}
            for obstacle in game["obstacle"]:
                obstacle_area = {"x": obstacle["x"]+20, "y": obstacle["y"]+20, "r": 20}
                if check_collision(obstacle_area, duck):
                    initial_state()
                    game["duck_num"]-=1
                    return
            for target in game["target"]:
                target_area = {"x": target["x"]+40, "y": target["y"]+75, "r": 40}
                if check_collision(target_area, duck):
                    game["target"].remove(target)
                    if not game["target"]:
                        if game["current_stage"] == "random.txt":
                            initial_state()
                            game["stage_num"]+=1
                            game["obstacle"]=[]
                            generate_random_map()
                        else:
                            game["win"] = True
                            gameover()

            if game["y"] <= 0:
                initial_state()
                game["duck_num"]-=1

def generate_random_object(width, height, radius, max_num, object_name):
    """
    Creates targets or obstacles randomly and
    add them to the game dictionary.
    These objects should be inside the window and under the upper interface.
    Avoids putting them around ducks.
    Prevents them from overlapping with or being put nearby themseleves.

    Parameters
    width, height, radius, object_name:
    objects' width, height, radius, name
    max_num: the max number of objects to put
    """
    num_object = random.randint(1,max_num)
    overlap = True
    for _ in range(num_object):
        while overlap:
            x = random.randint(0, WIN_WIDTH - width)
            y = random.randint(0, WIN_HEIGHT - height - 100)
            dic = {"x": x, "y": y, "r": radius}
            check_dic = {"x": dic["x"] + (width/2), "y": dic["y"]+ (height/2), "r": dic["r"]+40}
            overlap = check_random_collision(check_dic, radius)
        overlap = True
        game[object_name].append(dic)

def generate_random_map():
    """
    Calls generate_random_object function to generate random targets and obstacles.
    """
    generate_random_object(80, 150, 40, MAX_TARGET, "target")
    generate_random_object(40, 40, 20, MAX_OBSTACLE, "obstacle")

def check_random_collision(object_check, radius):
    """
    Checks if the input object overlaps with ducks, existing targets, or obstacles.
    If yes, return True, and If not, return False.
    """
    duck = {"x": game["x"]+20, "y": game["y"]+20, "r": 100}
    if check_collision(duck, object_check):
        return True
    for obstacle in game["obstacle"]:
        obstacle_area = {"x": obstacle["x"]+20, "y": obstacle["y"]+20, "r": radius+40}
        if check_collision(obstacle_area, object_check):
            return True
    for target in game["target"]:
        target_area = {"x": target["x"]+40, "y": target["y"]+75, "r": radius+40}
        if check_collision(target_area, object_check):
            return True
    return False

def stage():
    """
    Creates a game window and sets handler functions
    for keyboard, dragging, releasing, and drawing.
    Starts the game.
    """
    read_file(game["current_stage"])
    sweeperlib.set_draw_handler(draw_map)
    sweeperlib.set_keyboard_handler(keypress_map)
    sweeperlib.set_drag_handler(handle_drag)
    sweeperlib.set_release_handler(handle_release)

def random_stage():
    """
    Creates a game window and sets handler functions
    for keyboard, dragging, releasing, and drawing.
    Starts the game in random stage mode.
    """
    generate_random_map()
    sweeperlib.set_draw_handler(draw_map)
    sweeperlib.set_drag_handler(handle_drag)
    sweeperlib.set_keyboard_handler(keypress_map)
    sweeperlib.set_release_handler(handle_release)

def gameover():
    """
    Creates a window and sets handler functions
    for keyboard and drawing. Shows the result of the game.
    """
    game["playing"] = False
    sweeperlib.set_draw_handler(draw_result)
    sweeperlib.set_keyboard_handler(keypress_map)

def main_menu():
    """
    Creates a main menu window and sets handler functions
    for keyboard and drawing. Starts the application.
    """
    sweeperlib.set_draw_handler(draw_menu)
    sweeperlib.set_keyboard_handler(keypress_menu)


if __name__ == "__main__":
    sweeperlib.load_sprites("sprites")
    sweeperlib.load_duck("sprites")
    sweeperlib.create_window(width=WIN_WIDTH, height=WIN_HEIGHT)
    sweeperlib.set_interval_handler(flight)
    main_menu()
    sweeperlib.start()
