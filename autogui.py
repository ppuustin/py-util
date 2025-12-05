import pyautogui
import threading
import datetime

screenSize = pyautogui.size()

def moveMouse():
    pyautogui.moveTo(5, screenSize[1], duration = 1)

def clickMouse():
    pyautogui.click()
    main()

def main():
    hour = datetime.datetime.now().hour
    mins = datetime.datetime.now().minute
    if hour == 24 and mins == 50: # or hour == 12
        print("end of day reached")
        quit()
    else:
        threading.Timer(5.0, moveMouse).start()
        threading.Timer(10.0, clickMouse).start()

if __name__=="__main__":
    main()

'''
pyautogui
'''

