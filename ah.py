import time
import pyautogui
from win32gui import GetWindowText, GetForegroundWindow
import keyboard
import threading
import random

#coordinates
mailBoxLocation = (0,0)
postScan = (1229,525)
cancelScan = (1203,555)
post = (1682,558)
exit = (1133,92)
cancel = (1642,555)
openAllMail = (370,451)

#keybinds
relocateMailbox = ','
targetAH = 'num8'
openAh = 'num7'

#logic
run = False

#delay
ms = 0.1
lag = 1.5
interv = .6

#image recognition variables
lowConfidence = 0.7
mediumConfidence = 0.8
highConfidence = 0.9

#mailbox setter
def setMailboxLocation():
    global mailBoxLocation
    mailBoxLocation = pyautogui.position()
    print("Mailbox location set to: " + str(mailBoxLocation))

#keyboard input thread
def keyboard_input():
    while True:
        global run
        if keyboard.is_pressed(relocateMailbox):
            setMailboxLocation()
            time.sleep(1)
        if keyboard.is_pressed('.'):
            run = not run
            time.sleep(1)



def exitESC():
    print('exitESC')
    pyautogui.press('esc')

def openAH():
    print('openah')
    pyautogui.press(openAh)
    time.sleep(ms)
    pyautogui.press('multiply')
    time.sleep(ms)
    runPostScan()

def runCancelScann():
    global interv
    global lag
    pyautogui.moveTo(cancelScan[0],cancelScan[1],random.uniform(interv-0.2,interv+0.2))
    pyautogui.click()
    time.sleep(random.uniform(2,3))
    done_cancelling = pyautogui.locateOnScreen('done_cancelling.png',confidence=highConfidence)
    while done_cancelling == None : 
        pyautogui.moveTo(cancel[0],cancel[1],random.uniform(interv-0.2,interv+0.2))
        pyautogui.click()
        done_cancelling = pyautogui.locateOnScreen('done_cancelling.png',confidence=highConfidence)
        time.sleep(ms)
    pyautogui.moveTo(exit[0],exit[1],random.uniform(interv-0.2,interv+0.2))
    pyautogui.click()
    time.sleep(random.uniform(1,2))
    getMail()

def runPostScan():
    global interv
    global lag
    print('postscann')
    time.sleep(lag)
    pyautogui.moveTo(postScan[0],postScan[1],random.uniform(interv-0.2,interv+0.2))
    pyautogui.click()
    time.sleep(random.uniform(2,3))
    done_posting = pyautogui.locateOnScreen('done_posting.png',confidence=highConfidence)
    pyautogui.moveTo(post[0],post[1],random.uniform(interv-0.2,interv+0.2))
    while done_posting == None : 
        pyautogui.click()
        done_posting = pyautogui.locateOnScreen('done_posting.png',confidence=highConfidence)
        time.sleep(ms)
    pyautogui.moveTo(exit[0],exit[1],random.uniform(interv-0.2,interv+0.2))
    pyautogui.click()
    time.sleep(random.uniform(1,2))
    print('donePosting')
    runCancelScann()

def getMail():
    global lag
    global interv
    print('mailbox')
    pyautogui.moveTo(mailBoxLocation[0], mailBoxLocation[1],random.uniform(interv-0.2,interv+0.2))
    pyautogui.click()
    time.sleep(lag)
    no_open_mail = pyautogui.locateOnScreen('no_open_mail.png',confidence=highConfidence)
    counter = 0
    if no_open_mail == None :
        print('there are mails')
        pyautogui.moveTo(openAllMail[0],openAllMail[1],random.uniform(interv-0.2,interv+0.2))
        pyautogui.click()
    while no_open_mail == None :
        counter+=1
        no_open_mail = pyautogui.locateOnScreen('no_open_mail.png',confidence=highConfidence)
        time.sleep(ms+.5)
    print(counter-1)
    time.sleep(random.uniform(1,2))
    openAH()

if __name__ == "__main__":
    threadin = threading.Thread(target=keyboard_input)
    threadin.daemon = True
    threadin.start()
    while True :
        if GetWindowText(GetForegroundWindow()) == "World of Warcraft":
            if run:
                print('running')
                openAH()
