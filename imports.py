"""
All modules needed
"""

import os
import random # needed in logic
import numpy
from shutil import get_terminal_size # needed in gamestates/logic
from time import sleep # needed in gamestates
import pynput # needed in gamestates
from copy import deepcopy # needed in logic
from pyfiglet import Figlet # needed in utils
from itertools import zip_longest # needed in utils

menukeys = set()
settingskeys = set()
startkeys = set()
gameoverkeys = set()

def menu_on_press(key):
    menukeys.add(key)
def settings_on_press(key):
    settingskeys.add(key)
def gameover_on_press(key):
    gameoverkeys.add(key)

def menu_on_release(key):
    menukeys.remove(key)
def settings_on_release(key):
    settingskeys.remove(key)
def gameover_on_release(key):
    gameoverkeys.remove(key)

def keynormal(char):
    return pynput.keyboard.KeyCode.from_char(char)
def keyspecial(s):
    """space | enter | arrowup | arrowleft | arrowdown | arrowright"""
    return {"space": pynput.keyboard.Key.space,
            "enter": pynput.keyboard.Key.enter,
            "arrowup": pynput.keyboard.Key.up,
            "arrowleft": pynput.keyboard.Key.left,
            "arrowdown": pynput.keyboard.Key.down,
            "arrowright": pynput.keyboard.Key.right}.get(s, s)

menulistener =  pynput.keyboard.Listener(on_press=menu_on_press, on_release=menu_on_release)
settingslistener =  pynput.keyboard.Listener(on_press=settings_on_press, on_release=settings_on_release)
gameoverlistener =  pynput.keyboard.Listener(on_press=gameover_on_press, on_release=gameover_on_release)