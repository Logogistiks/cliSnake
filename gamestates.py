"""
Menu/UI functions for main
"""

from utils import *
from logic import Game
from ansi import *

def menu():
    screenX, screenY = 0, 0
    logo = headline("Snake")
    update = False
    while True:
        if get_terminal_size().columns != screenX or get_terminal_size().lines != screenY or update:
            if not update:
                hardClear()
            update = False
            screenX, screenY = get_terminal_size()
            centeredLogo = centerMultiline(logo, screenX)
            print(CMT + centeredLogo)
            print("Press Space to start Game".center(screenX))
            print("Press x to access Settings".center(screenX))
        if keyboard.is_pressed("space"):
            return
        if keyboard.is_pressed("x"):
            settings()
            print(CLR)
            update = True

def settings():
    SETTINGS_rendermode, SETTINGS_savehs, SETTINGS_speedadj = numpy.load("settings.npy", allow_pickle=True)
    colorDict = {True: COLOR_SETTINGS_FOREGROUND+COLOR_SETTINGS_BACKGROUND, False: COLORRESET+COLORRESET}
    screenX, screenY = 0, 0
    selection = 0
    print(CLR)
    update = False
    while True:
        if get_terminal_size().columns != screenX or get_terminal_size().lines != screenY or update:
            update = False
            screenX, screenY = get_terminal_size()
            print(CMT + "Settings".center(screenX))
            print("To navigate use arrow keys ↑↓, to select press enter <╝. Press c to cancel".center(screenX))
            print()
            print(f"Render mode: <{colorDict[selection==0]}{SETTINGS_rendermode[0][SETTINGS_rendermode[1]]}{COLORRESET}>".center(screenX))
            print(f"Save Highscore: <{colorDict[selection==1]}{SETTINGS_savehs[0][SETTINGS_savehs[1]]}{COLORRESET}>".center(screenX))
            print(f"increasing speed: <{colorDict[selection==2]}{SETTINGS_speedadj[0][SETTINGS_speedadj[1]]}{COLORRESET}>".center(screenX))
        if keyboard.is_pressed("up arrow"):
            selection = max(0, selection-1)
            while keyboard.is_pressed("up arrow"):
                pass
            update = True
        if keyboard.is_pressed("down arrow"):
            selection = min(2, selection+1)
            while keyboard.is_pressed("down arrow"):
                pass
            update = True
        if keyboard.is_pressed("enter"):
            match selection:
                case 0:
                    SETTINGS_rendermode = [SETTINGS_rendermode[0], 1-SETTINGS_rendermode[1]]
                case 1:
                    SETTINGS_savehs = [SETTINGS_savehs[0], 1-SETTINGS_savehs[1]]
                case 2:
                    SETTINGS_speedadj = [SETTINGS_savehs[0], 1-SETTINGS_speedadj[1]]
            while keyboard.is_pressed("enter"):
                pass
            update = True
        if keyboard.is_pressed("c"):
            numpy.save("settings", [SETTINGS_rendermode, SETTINGS_savehs, SETTINGS_speedadj])
            return

def start():
    SETTINGS_rendermode, SETTINGS_savehs, SETTINGS_speedadj = numpy.load("settings.npy", allow_pickle=True)
    detailedrender = SETTINGS_rendermode[1] == SETTINGS_rendermode[0].index("detailed")
    hardClear()
    screenX, screenY = 0, 0
    gameController = Game(20, 10*{True: 2, False: 1}[detailedrender])
    gameController.spawnTreat()
    keyboard.add_hotkey("w", gameController.changeDir, args=("w"))
    keyboard.add_hotkey("up arrow", gameController.changeDir, args=("w"))
    keyboard.add_hotkey("a", gameController.changeDir, args=("a"))
    keyboard.add_hotkey("left arrow", gameController.changeDir, args=("a"))
    keyboard.add_hotkey("s", gameController.changeDir, args=("s"))
    keyboard.add_hotkey("down arrow", gameController.changeDir, args=("s"))
    keyboard.add_hotkey("d", gameController.changeDir, args=("d"))
    keyboard.add_hotkey("right arrow", gameController.changeDir, args=("d"))
    while True:
        if gameController.move() == -1:
            keyboard.remove_all_hotkeys()
            return gameController.score
        if get_terminal_size().columns != screenX or get_terminal_size().lines != screenY:
            screenX, screenY = get_terminal_size()
            hardClear()
        print(CMT)
        gameController.displayGame()
        sleep(1/gameController.speed)

def gameover(score):
    SETTINGS_rendermode, SETTINGS_savehs, SETTINGS_speedadj = numpy.load("settings.npy", allow_pickle=True)
    screenX, screenY = 0, 0
    logo = headline("Game Over!")
    print(CLR)
    if SETTINGS_savehs[1] == SETTINGS_savehs[0].index("yes"):
        if os.path.exists("data.npy"):
            hs = numpy.load("data.npy")[0]
            if score > hs:
                numpy.save("data", [score])
        else:
            numpy.save("data", [score])
    while True:
        if get_terminal_size().columns != screenX or get_terminal_size().lines != screenY:
            screenX, screenY = get_terminal_size()
            centeredLogo = centerMultiline(logo, screenX)
            highscore = score
            if os.path.exists("data.npy"):
                read = numpy.load("data.npy")[0]
                if score > read:
                    numpy.save("data.npy", [score])
                else:
                    highscore = read
            else:
                numpy.save("data.npy", [score])
            print(CMT + centeredLogo)
            print(f"Score: {score}          Highscore: {highscore}".center(screenX))
            print()
            print("Press q to exit".center(screenX))
            print("Press r to restart".center(screenX))
        if keyboard.is_pressed("q"):
            exit()
        if keyboard.is_pressed("r"):
            return