from dependencyHandler import *

if not os.path.exists("settings.npy"):
    numpy.save("settings", [SETTINGS_rendermode, SETTINGS_savehs, SETTINGS_speedadj])

if __name__ == "__main__":
    while True:
        menu()
        score = start()
        gameover(score)
        print(CLR)