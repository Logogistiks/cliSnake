# cliSnake
This application brings the game Snake to the commandline, featuring both a minimalist mode and a detailed mode.

<p float="left">
  <img src="/images/screenshot_menu.png" width="450"/>
  <img src="/images/screenshot_gameover.png" width="450" /> 
</p>
<p float="left">
  <img src="/images/screenshot_game_simple.png" width="450" />
  <img src="/images/screenshot_game_detailed.png" width="450" /> 
</p>


## Prerequisites
* `python3` and `pip` installed
* `git` installed

## Installation
1. Clone the repository
```
git clone https://github.com/Logogistiks/cliSnake
```
\
2. Enter directory
```
cd cliSnake
```
\
3. Install requirements
```
pip install -r requirements.txt
```
\
4. Run game
```
python3 main.py
```

## How to play
In the menu, press `space` to start. \
To move, press `w` `a` `s` `d` or use the arrow keys `↑` `←` `↓` `→`. \
Collect the food to grow longer, but don't collide with yourself!

After you lose, press `q` to exit the game or `r` to get back to the menu.

In the menu, you can also press `x` to enter the settings. \
Here you can use the arrow keys `↑` `↓` to select an option. \
If you want to change an option, press enter `<┘`.

## Available Settings
| Option           | Description   |
| ---------------- |:-------------:|
| Render mode      | `simple` : Renders each cell as a single character<br>`detailed` : Renders each cell as a double character to simulate square pixels |
| Save Highscore   | `yes` : Saves highscore after every game,<br>`no` : No highscore gets saved |
| increasing speed | `yes` : Player speed increases proportional to score<br>`no` : Player speed stays the same all game |
