import threading
import tkinter as tk
import tkinter.font
import serial
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
import snowboydecoder
import sys
import signal

DETECT_TIMEOUT = 6
interrupted = False
interrupted2 = False
detectionflag = "None"


def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def true_terminate():
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted


MODEL_BM = "/home/pi/greyhound_pepsi/audio/tanpa kalori.pmdl"
MODEL_EN = "/home/pi/greyhound_pepsi/audio/Bold Taste.pmdl"

signal.signal(signal.SIGINT, signal_handler)


detectorEN = snowboydecoder.HotwordDetector(MODEL_EN, sensitivity=0.6)
detectorBM = snowboydecoder.HotwordDetector(MODEL_BM, sensitivity=0.6)

win = tk.Tk()
win.title("Greyhound Pepsi")
#win.attributes("-fullscreen", True)
myFont = tkinter.font.Font(family='Helvetica',size=12,weight="bold")
arduino = serial.Serial('/dev/ttyUSB0',9600)

PEAK = 2
videovar = "null" #Determines the video playing

FULL = Path("/home/pi/Desktop/projectvideo/full.mp4")
player1 = OMXPlayer(FULL,args=["-o", "hdmi", "--orientation","90","--loop","--no-osd"],dbus_name='org.mpris.MediaPlayer2.omxplayer0')

def gotdetect():
    global detectionflag
    detectionflag =  "Detected"
    trystop()

def detectBM():
    global interrupted
    interrupted = False
    print("--------------------SPAM BM STARTED-------------------")
    detectorBM.start(detected_callback=gotdetect, interrupt_check=interrupt_callback, sleep_time=0.03)
    detectorBM.terminate()
    print("--------------------SPAM BM ENDED-------------------")

def detectEN():
    global interrupted
    interrupted = False
    print("--------------------SPAM EN STARTED------------------")
    detectorEN.start(detected_callback=gotdetect, interrupt_check=interrupt_callback, sleep_time=0.03)
    detectorEN.terminate()
    print("------------------- SPAM EN ENDED-----------------------")
    
def trystop():
    global interrupted
    true_terminate()
    print("Try stopping done....")


def timeout():
    global detectionflag
    while(True):
        timeoutflag.wait()
        timeoutflag.clear()
        print("Timeout flag started")
        sleep(DETECT_TIMEOUT)
        print("Timeout Ended")
        print("Timeout set since none")
        if(detectionflag == "None"):
            detectionflag = "Timeout"
            trystop()

def looper(starttime,videoname,endtime):
    print("Looper active")
    print("Video name: "+videoname)
    print("Start pos: "+str(starttime))
    global videovar
    while(True):
        sleep(0.01)
        currentvidtime=player1.position()
        if(currentvidtime>=endtime):
            player1.set_position(starttime)
        if(videoname!=videovar):
            print("Video changed!")
            break

def seeking():
    global videovar
    print("Seeking thread started")
    sleep(1)
    print(videovar)
    while(True):
        sleep(1)
        print(videovar)

        if(videovar=="language"):
            starttime=0
            duration=9
            player1.set_position(starttime)
            endtime=starttime+duration
            looper(starttime,"language",endtime)
    
        if(videovar=="phrase1en"):
            starttime=12
            duration=10
            player1.set_position(starttime)
            endtime=starttime+duration
            looper(starttime,"phrase1en",endtime)

        if(videovar=="phrase2en"):
            starttime=23
            duration=12
            player1.set_position(starttime)
            endtime=starttime+duration
            looper(starttime,"phrase2en",endtime)

        if(videovar=="phrase1bm"):
            starttime=59
            duration=7
            player1.set_position(starttime)
            endtime=starttime+duration
            looper(starttime,"phrase1bm",endtime)

        if(videovar=="phrase2bm"):
            starttime=70
            duration=16
            player1.set_position(starttime)
            endtime=starttime+duration
            looper(starttime,"phrase2bm",endtime)

        if(videovar=="dispense"):
            starttime=41
            duration=14
            player1.set_position(starttime)
            endtime=starttime+duration
            looper(starttime,"dispense",endtime)

        if(videovar=="idle"):
            starttime=91
            duration=5
            player1.set_position(starttime)
            endtime=starttime+duration
            looper(starttime,"idle",endtime)

def mainseries():
    global videovar
    while(True):
        enableStart()
        disableBM()
        disableEN()
        videovar = "idle"
        startblock.wait()
        startblock.clear()
        disableStart()
        enableBM()
        enableEN()
        videovar = "language"
        mainseriesblock.wait()
        mainseriesblock.clear()
 
def en():
    while(True):
        enblock.wait()
        enblock.clear()
        trystop()
        global detectionflag
        detectionflag = "None"
        print("English Mode entered")
        global videovar
        attempts = 0
        videovar = "phrase1en"
        sleep(10)
        videovar = "phrase2en"
        print("ENGLISH STARTED")
        while(attempts < 3):
            detectionflag = "None"
            print(".........")
            if(attempts >= 1):
                sleep(3.5)
            print("Waiting for sound... ")
            timeoutflag.set()
            detectEN()  #Blocking
            print("DETECTION FLAG: " + detectionflag)
            if(detectionflag == "Detected"):
                sleep(2)
                videovar = "dispense"
                sleep(12.5)
                print("DISPENSED")
                arduino.write(b'd')
                sleep(1)
                break
            if(detectionflag == "Timeout"):
                print("Timeout detected")
                detectionflag = "None"
            attempts += 1
            print("Attempt: "+str(attempts))
        detectionflag = "None"
        attempts = 0
        trystop()
        mainseriesblock.set()


def bm():
    while(True):
        bmblock.wait()
        bmblock.clear()
        trystop()
        global detectionflag
        detectionflag = "None"
        print("BM Mode entered")
        global videovar
        attempts = 0
        videovar = "phrase1bm"
        sleep(6.7)
        videovar = "phrase2bm"
        print("BAHASA STARTED")
        while(attempts < 3):
            detectionflag = "None"
            print(".........")
            if(attempts >= 1):
                sleep(8.5)
            print("Waiting for sound... ")
            timeoutflag.set() 
            detectBM()  #Blocking
            print("DETECTION FLAG: " + detectionflag)
            if(detectionflag == "Detected"):
                sleep(2)
                videovar = "dispense"
                sleep(14)
                print("DISPENSED")
                arduino.write(b'd')
                sleep(1)
                break
            if(detectionflag == "Timeout"):
                print("Timeout detected")
                detectionflag = "None"
            attempts += 1
            print("Attempt: "+str(attempts))
        detectionflag = "None"
        attempts = 0
        trystop()
        mainseriesblock.set()

def unblockbm():
    print("BM START ISSUED")
    bmblock.set()

def unblocken():
    print("EN START ISSUED")
    enblock.set()

def unblockstart():
    startblock.set()

def disableBM():
    bmbutton.config(state=tk.DISABLED)

def enableBM():
    bmbutton.config(state=tk.NORMAL)

def disableEN():
    enbutton.config(state=tk.DISABLED)

def enableEN():
    enbutton.config(state=tk.NORMAL)

def disableStart():
    startbutton.config(state=tk.DISABLED)
    startbutton2.config(state=tk.DISABLED)

def enableStart():
    startbutton.config(state=tk.NORMAL)
    startbutton2.config(state=tk.NORMAL)



mainseriesblock=threading.Event()
timeoutflag=threading.Event()
bmblock=threading.Event()
enblock=threading.Event()
startblock=threading.Event()

threadseeking = threading.Thread(target=seeking)
threadmainseries=threading.Thread(target=mainseries)
threadtimeout = threading.Thread(target=timeout)
threaden = threading.Thread(target=en)
threadbm = threading.Thread(target=bm)


bmbutton = tk.Button(win, text="BM", font=myFont, command=unblockbm, height=5, width=5)
bmbutton.grid(row=2, column=2, sticky=tk.NSEW)
enbutton = tk.Button(win, text="EN", font=myFont, command=unblocken, height=5, width=5)
enbutton.grid(row=1, column=2, sticky=tk.NSEW)
startbutton = tk.Button(win, text="START", font=myFont, command=unblockstart, height=5, width=5)
startbutton.grid(row=1, column=1, sticky=tk.NSEW)
startbutton2 = tk.Button(win, text="START", font=myFont, command=unblockstart, height=5, width=5)
startbutton2.grid(row=2, column=1, sticky=tk.NSEW)


if __name__ == '__main__':
    threadtimeout.start()
    threadmainseries.start()
    threadseeking.start()
    threadbm.start()
    threaden.start()
    win.mainloop()

