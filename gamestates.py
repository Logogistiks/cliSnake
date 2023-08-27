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
    with menulistener:
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
            if keyspecial("space") in menukeys:
                while keyspecial("space") in menukeys:
                    pass
                return
            if keynormal("x") in menukeys:
                while keynormal("x") in menukeys:
                    pass
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
    with settingslistener:
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
            if keyspecial("arrowup") in settingskeys:
                while keyspecial("arrowup") in settingskeys:
                    pass
                selection = max(0, selection-1)
                update = True
            if keyspecial("arrowdown") in settingskeys:
                while keyspecial("arrowdown") in settingskeys:
                    pass
                selection = min(2, selection+1)
                update = True
            if keyspecial("enter") in settingskeys:
                while keyspecial("enter") in settingskeys:
                    pass
                match selection:
                    case 0:
                        SETTINGS_rendermode = [SETTINGS_rendermode[0], 1-SETTINGS_rendermode[1]]
                    case 1:
                        SETTINGS_savehs = [SETTINGS_savehs[0], 1-SETTINGS_savehs[1]]
                    case 2:
                        SETTINGS_speedadj = [SETTINGS_savehs[0], 1-SETTINGS_speedadj[1]]
                update = True
            if keynormal("c") in settingskeys:
                while keynormal("c") in settingskeys:
                    pass
                numpy.save("settings", [SETTINGS_rendermode, SETTINGS_savehs, SETTINGS_speedadj])
                return

def start():
    SETTINGS_rendermode, SETTINGS_savehs, SETTINGS_speedadj = numpy.load("settings.npy", allow_pickle=True)
    detailedrender = SETTINGS_rendermode[1] == SETTINGS_rendermode[0].index("detailed")
    hardClear()
    screenX, screenY = 0, 0
    gameController = Game(20, 10*{True: 2, False: 1}[detailedrender])
    gameController.spawnTreat()
    def gameonpress(key):
        if key == keynormal("w"):
            gameController.changeDir("w")
        if key == keyspecial("arrowup"):
            gameController.changeDir("w")
        if key == keynormal("a"):
            gameController.changeDir("a")
        if key == keyspecial("arrowleft"):
            gameController.changeDir("a")
        if key == keynormal("s"):
            gameController.changeDir("s")
        if key == keyspecial("arrowdown"):
            gameController.changeDir("s")
        if key == keynormal("d"):
            gameController.changeDir("d")
        if key == keyspecial("arrowright"):
            gameController.changeDir("d")
    def gameonrelease(key):
        pass
    gamelistener = pynput.keyboard.Listener(on_press=gameonpress, on_release=gameonrelease)
    with gamelistener:
        while True:
            if gameController.move() == -1:
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
    with gameoverlistener:
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
            if keynormal("q") in gameoverkeys:
                exit()
            if keynormal("r") in gameoverkeys:
                while keynormal("r") in gameoverkeys:
                    pass
                return