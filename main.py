import os
import random
import numpy
from shutil import get_terminal_size
from time import sleep
import keyboard
from copy import deepcopy
from pyfiglet import Figlet

def hardClear():
    os.system("clear" if os.name == "posix" else "cls")

def stripAnsi(s: str):
    ansiChars = [r"\x1b[92m", r"\x1b[93m", r"\x1b[91m", r"\x1b[96m", r"\x1b[0m"]
    newstr = s
    for ansi in ansiChars:
        newstr.replace(ansi, "")
    return newstr

CMT = "\033[H"
CLR = "\033[2J"
COLOR_SETTINGS_BACKGROUND = "\033[47m" # white
COLOR_SETTINGS_FOREGROUND = "\033[30m" # black
COLORRESET = "\033[00m"

SETTINGS_rendermode = [["simple", "detailed"], 0]
SETTINGS_savehs = [["yes", "no"], 0]
SETTINGS_speedadj = [["yes", "no"], 0]
if os.path.exists("settings.npy"):
    SETTINGS_rendermode, SETTINGS_savehs, SETTINGS_speedadj = numpy.load("settings.npy", allow_pickle=True)

def looparound(n, lower, upper):
    return (n - lower) % (upper - lower + 1) + lower

def equalizeljustMultiline(s: str, char: str=" "):
    lines = s.split("\n")
    maxlen = max(map(len, lines))
    return "\n".join(line.ljust(maxlen - len(line), char) for line in lines)

def centerMultiline(s: str, w: int, dir: str="left", char: str=" "):
    lines = equalizeljustMultiline(s, char).split("\n")
    l = len(lines[0]) # all lines same length
    missing = w - l
    if missing % 2 == 0: # even
        left = right = " "*(missing//2)
    else:
        left = " "*(missing//2+1*(dir!="left"))
        right = " "*(missing//2+1*(dir != "right"))
    lines = list(map(lambda x: left+x+right, lines))
    return "\n".join(lines)

def listReplace(lst: list[str], search: str, replacement: str):
    return list(map(lambda x: x.replace(search, replacement), lst))

def listReplace2d(lst: list[list[str]], search: str, replacement: str):
    return [listReplace(x) for x in lst]

def listReplaceDict(lst: list[str], dct: dict):
    return list(map(lambda x: dct[x], lst))

def listReplaceDict2d(lst: list[list[str]], dct: dict):
    return [listReplaceDict(x, dct) for x in lst]

def listConvert(lst: list):
    return list(map(str, lst))

def listConvert2d(lst: list[list]):
    return [listConvert(x) for x in lst]

def trailingSpaceMultiline(s: str):
    whiteSpace = []
    for line in s.split("\n"):
        whiteSpace.append(" "*(len(line)-len(line.rstrip())))
    return whiteSpace

def leadingSpaceMultiline(s: str):
    whiteSpace = []
    for line in s.split("\n"):
        whiteSpace.append(" "*(len(line)-len(line.lstrip())))
    return whiteSpace

def AddStrLst(l1: list[str], l2: list[str]):
        maxlen = max(len(l1), len(l2))
        l1pad = l1 + [""]*(maxlen-len(l1))
        l2pad = l2 + [""]*(maxlen-len(l2))
        return [el1+el2 for el1, el2 in list(zip(l1pad, l2pad))]

def headline(text, font="doom"):
    CustomFig = Figlet(font=font)
    logo = CustomFig.renderText(text)
    return logo

class Game:
    def __init__(self, sizeX, sizeY, baseSpeed=1):
        """
        0: empty
        1: up
        2: left
        3: down
        4: right
        5: treat
        """
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.grid = [[0]*sizeX for _ in range(sizeY)]
        self.lastHeadPos = [sizeY//2, sizeX//2]
        self.grid[self.lastHeadPos[0]][self.lastHeadPos[1]] = 1
        self.score = 0
        self.baseSpeed = baseSpeed
        self.speed = baseSpeed
        self.renderCharsSimple =  {"0": " ", "1": "█", "2": "█", "3": "█", "4": "█", "5": "▓"}
        self.renderCharsDetailed = {"0": "  ", "1": "██", "2": "██", "3": "██", "4": "██", "5": "▓▓"}
        self.dirmap = {"w": 1, "a": 2, "s": 3, "d": 4}
        self.invdirmap = {1: 3, 2: 4, 3: 1, 4: 2}
        self.COLORHEAD =  "\033[92m" # lightgreen
        self.COLORBODY =  "\033[93m" # yellow
        self.COLORTREAT = "\033[91m" # lightred
        self.COLORSCORE = "\033[96m" # lightcyan
        self.COLORRESET = "\033[0m" # reset

    def gridLimit(self):
        return [0, 0, self.sizeY-1, self.sizeX-1]

    def spawnTreat(self):
        possible = self.gridFindAll([0])
        treatY, treatX = random.choice(possible)
        self.grid[treatY][treatX] = 5

    def gridFindAll(self, t: list):
        pos = []
        for y, row in enumerate(self.grid):
            for x, value in enumerate(row):
                if value in t:
                    pos.append([y, x])
        return pos if pos else None

    def gridFindAny(self, t: list):
        for y, row in enumerate(self.grid):
            for x, value in enumerate(row):
                if value in t:
                    return [y, x]
        return None

    def outOfBounds(self, y, x):
        if 0 <= y <= self.sizeY-1 and 0 <= x <= self.sizeX:
            return False
        else:
            return True

    def newPos(self, y, x, dir, ly, lx, uy, ux):
        newY = y + (dir==3) - (dir==1)
        newX = x + (dir==4) - (dir==2)
        return [looparound(newY, ly, uy), looparound(newX, lx, ux)]

    def findHead(self):
        next = self.gridFindAny([1, 2, 3, 4])
        known = []
        while True:
            current = next
            if current in known:
                return self.newPos(self.lastHeadPos[0], self.lastHeadPos[1], self.grid[self.lastHeadPos[0]][self.lastHeadPos[1]], *self.gridLimit())
            known.append(current)
            currentdir = self.grid[current[0]][current[1]]
            next = self.newPos(current[0], current[1], currentdir, *self.gridLimit())
            if self.grid[next[0]][next[1]] not in [1, 2, 3, 4]:
                self.lastHeadPos = current
                return current

    def findTail(self):
        def isTail(y, x):
            adjs = getAdjValues(y, x)
            return adjs[0] != 3 and adjs[1] != 4 and adjs[2] != 1 and adjs[3] != 2
        def findPrev(y, x):
            if isTail(y, x):
                return None
            adjs = getAdj(y, x)
            adjvals = getAdjValues(y, x)
            if adjvals[0] == 3:
                return adjs[0]
            elif adjvals[1] == 4:
                return adjs[1]
            elif adjvals[2] == 1:
                return adjs[2]
            elif adjvals[3] == 2:
                return adjs[3]
        def getAdj(y, x):
            return [self.newPos(y, x, 1, *self.gridLimit()), # up
                    self.newPos(y, x, 2, *self.gridLimit()), # left
                    self.newPos(y, x, 3, *self.gridLimit()), # down
                    self.newPos(y, x, 4, *self.gridLimit())] # right
        def getAdjValues(y, x):
            return [self.grid[k[0]][k[1]] for k in getAdj(y, x)]
        next = self.findHead()
        while True:
            current = next
            next = findPrev(current[0], current[1])
            if next is None:
                return [current[0], current[1]]

    def findDir(self):
        headpos = self.findHead()
        return self.grid[headpos[0]][headpos[1]]

    def changeDir(self, dir: str):
        currentpos = self.findHead()
        currentdir = self.grid[currentpos[0]][currentpos[1]]
        if self.invdirmap[self.dirmap[dir]] == currentdir: # left in for case snake length = 1
            return
        potentialPos = self.newPos(currentpos[0], currentpos[1], self.dirmap[dir], *self.gridLimit())
        if self.grid[potentialPos[0]][potentialPos[1]] in [1,2,3,4]: # body
            return
        self.grid[currentpos[0]][currentpos[1]] = self.dirmap[dir]

    def move(self):
        if SETTINGS_speedadj[1] == SETTINGS_speedadj[0].index("yes"):
            self.speed = self.baseSpeed + 0.5*self.score
        currentpos = self.findHead()
        currentdir = self.grid[currentpos[0]][currentpos[1]]
        nextpos = self.newPos(currentpos[0], currentpos[1], currentdir, *self.gridLimit())
        if self.grid[nextpos[0]][nextpos[1]] in [1, 2, 3, 4]: # own tail
            return -1
        else:
            if self.grid[nextpos[0]][nextpos[1]] == 5: # treat
                self.score += 1
                self.spawnTreat()
            else: # move tailpiece
                tailpos = self.findTail()
                self.grid[tailpos[0]][tailpos[1]] = 0
            self.grid[nextpos[0]][nextpos[1]] = currentdir # move headpiece

    def renderGrid(self):
        charset = {True: self.renderCharsSimple, False: self.renderCharsDetailed}[SETTINGS_rendermode[1] == SETTINGS_rendermode[0].index("simple")]
        headpos = self.findHead()
        rendered = deepcopy(self.grid)
        rendered = listConvert2d(rendered)
        rendered = listReplaceDict2d(rendered, charset)
        renderedColor = deepcopy(rendered)
        for j, y in enumerate(rendered):
            for i, x in enumerate(y):
                if x in [charset[k] for k in "1234"]:
                    if [j, i] == headpos:
                        renderedColor[j][i] = self.COLORHEAD + rendered[j][i] + self.COLORRESET
                    else:
                        renderedColor[j][i] = self.COLORBODY + rendered[j][i] + self.COLORRESET
                if x == charset["5"]:
                    renderedColor[j][i] = self.COLORTREAT + rendered[j][i] + self.COLORRESET
        return ("\n".join("".join(row) for row in rendered), "\n".join("".join(row) for row in renderedColor))

    def displayGame(self):
        detailedrender = SETTINGS_rendermode[1] == SETTINGS_rendermode[0].index("detailed")
        borderChars = {"vertical": "║",
                       "horizontal": "═",
                       "junction": {"left": "╠",
                                    "right": "╣",
                                    "top": "╦",
                                    "bot": "╩",
                                    "center": "╬"},
                       "left": {"top": "╔",
                                "bot": "╚"},
                       "right": {"top": "╗",
                                 "bot": "╝"}}
        boardA = [] # normal
        boardwoA = [] # without Ansi
        renderwoA, renderA = self.renderGrid()[0].split("\n"), self.renderGrid()[1].split("\n")
        for i in range(len(renderA)):
            newlineA = borderChars["vertical"] + renderA[i]
            newlinewoA = borderChars["vertical"] + renderwoA[i]
            match i:
                case 0:
                    newlineA += borderChars["vertical"] + self.COLORSCORE + str(self.score).center(max(5, len(str(self.score)))) + self.COLORRESET + borderChars["vertical"]
                    newlinewoA += borderChars["vertical"] + str(self.score).center(max(5, len(str(self.score)))) + borderChars["vertical"]
                case 1:
                    newlineA += borderChars["junction"]["left"] + borderChars["horizontal"]*max(5, len(str(self.score))) + borderChars["right"]["bot"]
                    newlinewoA += borderChars["junction"]["left"] + borderChars["horizontal"]*max(5, len(str(self.score))) + borderChars["right"]["bot"]
                case _:
                    newlineA += borderChars["vertical"]
                    newlinewoA += borderChars["vertical"]
            boardA.append(newlineA)
            boardwoA.append(newlinewoA)
        newlineA = borderChars["left"]["top"] + borderChars["horizontal"]*(self.sizeX*({True: 2, False: 1}[detailedrender]))
        newlinewoA = borderChars["left"]["top"] + borderChars["horizontal"]*(self.sizeX*({True: 2, False: 1}[detailedrender]))
        newlineA += borderChars["junction"]["top"] + borderChars["horizontal"]*max(5, len(str(self.score))) + borderChars["right"]["top"]
        newlinewoA += borderChars["junction"]["top"] + borderChars["horizontal"]*max(5, len(str(self.score))) + borderChars["right"]["top"]
        boardA.insert(0, newlineA)
        boardwoA.insert(0, newlinewoA)
        newlineA = borderChars["left"]["bot"] + borderChars["horizontal"]*(self.sizeX*({True: 2, False: 1}[detailedrender])) + borderChars["right"]["bot"]
        newlinewoA = borderChars["left"]["bot"] + borderChars["horizontal"]*(self.sizeX*({True: 2, False: 1}[detailedrender])) + borderChars["right"]["bot"]
        boardA.append(newlineA)
        boardwoA.append(newlinewoA)
        boardwoA = "\n".join(boardwoA)
        centered = centerMultiline(boardwoA, get_terminal_size()[0])
        leadSpace = leadingSpaceMultiline(centered)
        trailSpace = trailingSpaceMultiline(centered)
        final = "\n".join(AddStrLst(AddStrLst(leadSpace, boardA), trailSpace))
        print(final)

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
    global SETTINGS_rendermode, SETTINGS_savehs, SETTINGS_speedadj
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
    screenX, screenY = 0, 0
    logo = headline("Game Over!")
    print(CLR)
    if SETTINGS_savehs[1] == SETTINGS_savehs[0].index("yes"):
        numpy.save("data", [score])
    while True:
        if get_terminal_size().columns != screenX or get_terminal_size().lines != screenY:
            screenX, screenY = get_terminal_size()
            centeredLogo = centerMultiline(logo, screenX)
            print(CMT + centeredLogo)
            print(f"Score: {score}".center(screenX))
            print("Press q to exit".center(screenX))
            print("Press r to restart".center(screenX))
        if keyboard.is_pressed("q"):
            exit()
        if keyboard.is_pressed("r"):
            return

if __name__ == "__main__":
    while True:
        menu()
        score = start()
        gameover(score)
        print(CLR)