"""
Some utility functions for main
"""

from imports import *

def looparound(n: int, lower: int, upper: int):
    """
    Performs a loop-around operation on a number within a specified range.

    Args:
        n (int): The input number.
        lower (int): The lower bound of the range.
        upper (int): The upper bound of the range.

    Returns:
        int: The result of the loop-around operation.
    """
    return (n - lower) % (upper - lower + 1) + lower

def equalizeljustMultiline(s: str, char: str=" "):
    """
    Adjusts the left justification of each line in a multiline string to equalize their lengths.

    Args:
        s (str): The input multiline string.
        char (str, optional): The character used for padding. Defaults to space (" ").

    Returns:
        str: A multiline string with equalized left justification.
    """
    lines = s.split("\n")
    maxlen = max(map(len, lines))
    return "\n".join(line.ljust(maxlen - len(line), char) for line in lines)

def centerMultiline(s: str, w: int, dir: str="left", char: str=" "):
    """
    Centers each line in a multiline string within a specified width.

    Args:
        s (str): The input multiline string.
        w (int): The desired width for centering.
        dir (str, optional): The direction for centering if the strings have an odd length ("left" or "right"). Defaults to "left".
        char (str, optional): The character used for padding. Defaults to space (" ").

    Returns:
        str: A multiline string with centered lines.
    """
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
    """
    Replaces occurrences of a search string with a replacement string in a list of strings.

    Args:
        lst (list[str]): The input list of strings.
        search (str): The string to search for.
        replacement (str): The string to replace with.

    Returns:
        list[str]: A new list with replaced strings.
    """
    return [x.replace(search, replacement) for x in lst]

def listReplace2d(lst: list[list[str]], search: str, replacement: str):
    """
    Replaces occurrences of a search string with a replacement string in a 2D list of strings.

    Args:
        lst (list[list[str]]): The input 2D list of strings.
        search (str): The string to search for.
        replacement (str): The string to replace with.

    Returns:
        list[list[str]]: A new 2D list with replaced strings.
    """
    return [listReplace(x, search, replacement) for x in lst]

def listReplaceDict(lst: list[str], dct: dict):
    """
    Replaces strings in a list according to a dictionary's values.

    Args:
        lst (list[str]): The input list of strings.
        dct (dict): A dictionary where keys are strings to be replaced and values are their replacements.

    Returns:
        list[str]: A new list with replaced strings.
    """
    return [dct.get(x, x) for x in lst]

def listReplaceDict2d(lst: list[list[str]], dct: dict):
    """
    Replaces strings in a 2D list according to a dictionary's values.

    Args:
        lst (list[list[str]]): The input 2D list of strings.
        dct (dict): A dictionary where keys are strings to be replaced and values are their replacements.

    Returns:
        list[list[str]]: A new 2D list with replaced strings.
    """
    return [listReplaceDict(x, dct) for x in lst]

def listConvert(lst: list):
    """
    Converts elements of a list to strings.

    Args:
        lst (list): The input list.

    Returns:
        list[str]: A new list containing string representations of the original elements.
    """
    return list(map(str, lst))

def listConvert2d(lst: list[list]):
    """
    Converts elements of a 2D list to strings.

    Args:
        lst (list[list]): The input 2D list.

    Returns:
        list[list[str]]: A new 2D list containing string representations of the original elements.
    """
    return list(map(listConvert, lst))

def trailingSpaceMultiline(s: str):
    """
    Returns the trailing spaces for each line in a multiline string.

    Args:
        s (str): The input multiline string.

    Returns:
        list[str]: A list of trailing space strings corresponding to each line.
    """
    return [" "*(len(line) - len(line.rstrip())) for line in s.split("\n")]

def leadingSpaceMultiline(s: str):
    """
    Returns the leading spaces for each line in a multiline string.

    Args:
        s (str): The input multiline string.

    Returns:
        list[str]: A list of leading space strings corresponding to each line.
    """
    return [" "*(len(line) - len(line.lstrip())) for line in s.split("\n")]

def AddStrLst(l1: list[str], l2: list[str]):
    """
    Adds corresponding elements from two lists of strings, padding with empty strings if necessary.

    Args:
        l1 (list[str]): The first list of strings.
        l2 (list[str]): The second list of strings.

    Returns:
        list[str]: A new list containing concatenated strings.
    """
    return [el1 + el2 for el1, el2 in zip_longest(l1, l2, fillvalue="")]

def headline(text: str, font: str="doom"):
    """
    Generates a stylized text headline using a specified font.

    Args:
        text (str): The text to render as a headline.
        font (str, optional): The font style for rendering. Defaults to "doom".

    Returns:
        str: The stylized text as a headline.
    """
    CustomFig = Figlet(font=font)
    return CustomFig.renderText(text)

def hardClear():
    os.system("clear" if os.name == "posix" else "cls")