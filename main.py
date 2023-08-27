from dependencyHandler import *

if not os.path.exists("settings.json"):
    with open("settings.json", "w") as f:
        f.write(json.dumps([SETTINGS_rendermode, SETTINGS_savehs, SETTINGS_speedadj], indent=4))

if __name__ == "__main__":
    while True:
        menu()
        score = start()
        gameover(score)
        print(CLR)