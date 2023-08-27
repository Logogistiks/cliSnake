"""
The game logic for main
"""

from utils import *
from ansi import *

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
        with open("settings.json", "r") as f:
            self.SETTINGS_rendermode, self.SETTINGS_savehs, self.SETTINGS_speedadj = json.load(f)

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
        if self.SETTINGS_speedadj[1] == self.SETTINGS_speedadj[0].index("yes"):
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
        charset = {True: self.renderCharsSimple, False: self.renderCharsDetailed}[self.SETTINGS_rendermode[1] == self.SETTINGS_rendermode[0].index("simple")]
        headpos = self.findHead()
        rendered = deepcopy(self.grid)
        rendered = listConvert2d(rendered)
        rendered = listReplaceDict2d(rendered, charset)
        renderedColor = deepcopy(rendered)
        for j, y in enumerate(rendered):
            for i, x in enumerate(y):
                if x in [charset[k] for k in "1234"]:
                    if [j, i] == headpos:
                        renderedColor[j][i] = COLORHEAD + rendered[j][i] + COLORRESET
                    else:
                        renderedColor[j][i] = COLORBODY + rendered[j][i] + COLORRESET
                if x == charset["5"]:
                    renderedColor[j][i] = COLORTREAT + rendered[j][i] + COLORRESET
        return ("\n".join("".join(row) for row in rendered), "\n".join("".join(row) for row in renderedColor))

    def displayGame(self):
        detailedrender = self.SETTINGS_rendermode[1] == self.SETTINGS_rendermode[0].index("detailed")
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
                    newlineA += borderChars["vertical"] + COLORSCORE + str(self.score).center(max(5, len(str(self.score)))) + COLORRESET + borderChars["vertical"]
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