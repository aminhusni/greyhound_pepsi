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

DETECT_TIMEOUT = 8
interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

def gotdetect():
    global detectionflag
    detectionflag =  "Detected"
    try:
        stopEN()
    except:
        pass
    try:
        stopBM()
    except:
        pass

MODEL_BM = "/home/pi/greyhound_pepsi/audio/Rasa kola hebat.pmdl"
MODEL_EN = "/home/pi/greyhound_pepsi/audio/Bold Taste.pmdl"

signal.signal(signal.SIGINT, signal_handler)

detectorBM = snowboydecoder.HotwordDetector(MODEL_BM, sensitivity=0.6)
detectorEN = snowboydecoder.HotwordDetector(MODEL_EN, sensitivity=0.6)

detectionflag = "None"

win = tk.Tk()
win.title("Greyhound Pepsi")
#win.attributes("-fullscreen", True)
myFont = tkinter.font.Font(family='Helvetica',size=12,weight="bold")
arduino = serial.Serial('/dev/ttyUSB0',9600)

PEAK = 2
videovar = "null" #Determines the video playing

FULL = Path("/home/pi/Desktop/projectvideo/full.mp4")
player1 = OMXPlayer(FULL,args=["-o", "hdmi", "--orientation","0","--loop","--no-osd"],dbus_name='org.mpris.MediaPlayer2.omxplayer0')

def detectBM():
    print("--------------------SPAM-------------------")
    detectorBM.start(detected_callback=gotdetect, interrupt_check=interrupt_callback, sleep_time=0.03)
    print("--------------------SPAM-------------------")

def stopBM():
    detectorBM.terminate()

def detectEN():
    print("--------------------SPAM-------------------")
    detectorEN.start(detected_callback=gotdetect, interrupt_check=interrupt_callback, sleep_time=0.03)
    print("--------------------SPAM-------------------")

def stopEN():
    detectorEN.terminate()

def timeout():
    while(True):
        timeoutflag.wait()
        timeoutflag.clear()
        print("Timeout flag started")
        global detectionflag
        sleep(DETECT_TIMEOUT)
        print("Timeout Ended")
        if(detectionflag == "None"):
            detectionflag = "Timeout"
            try:
                stopEN()
            except:
                pass
            try:
                stopBM()
            except:
                pass

def looper(starttime,videoname,endtime):
    print("Looper active")
    print("Video name: "+videoname)
    print("Start pos: "+str(starttime))
    global videovar
    while(True):
        sleep(0.01)
        currentvidtime=player1.position()
        if(currentvidtime>=endtime):
#            print("Relooping back to:"+str(starttime))
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
#        print("From seeking thread:")
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
            starttime=68
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
            


def mainseries():
    global videovar
    while(True):
        videovar = "language"
        mainseriesblock.wait() 
        mainseriesblock.clear()
 
def en():
    global detectionflag
    print("English Mode entered")
    global videovar
    attempts = 0
    videovar = "phrase1en"
    sleep(10)
    videovar = "phrase2en"
    print("ENGLISH STARTED")
    PEAK = 2
    while(True):
        print(".........")
        if(attempts >= 1):
            sleep(2)
        print("Waiting for sound... ")
        timeoutflag.set()
        detectEN()
        print(detectionflag)
        if(detectionflag == "Detected"):
            videovar = "dispense"
            sleep(12.5)
            print("DISPENSED")
            arduino.write(b'd')
            sleep(1)
            break
            break
        if(detectionflag == "Timeout"):
            break
        attempts += 1
        PEAK = 1
        print("Attempt: "+str(attempts))
    detectionflag = "None"
    attempts = 0
    mainseriesblock.set()

def bm():
    global detectionflag
    print("BM Mode entered")
    global videovar
    attempts = 0
    videovar = "phrase1bm"
    sleep(7)
    videovar = "phrase2bm"
    PEAK = 2
    while(True):
        print("......")
        if(attempts >= 1):
            sleep(6)
        print("Waiting for sound... ")
        arduino.write(b'v')
        val1 = arduino.readline()
        val2 = arduino.readline()
        total = int(val1) + int(val2)
        print("Total DETECTED was "+str(total))
        if(total >= PEAK):
            videovar = "dispense"
            sleep(14)
            print("DISPENSED")
            arduino.write(b'd')
            sleep(1)
            break
        attempts += 1
        PEAK = 1
        print("Attempt: "+str(attempts))
        if(attempts >= 3):
            sleep(15.5)
            videovar = "dispense"
            sleep(14)
            print("DISPENSED")
            arduino.write(b'd')
            sleep(1)
            break
    attempts = 0
    mainseriesblock.set()



mainseriesblock=threading.Event()
timeoutflag=threading.Event()

threadseeking = threading.Thread(target=seeking)
threadmainseries=threading.Thread(target=mainseries)
threadtimeout = threading.Thread(target=timeout)

bmbutton = tk.Button(win, text="BM", font=myFont, command=bm, height=80, width=105)
bmbutton.grid(row=1, column=1, sticky=tk.NSEW)
enbutton = tk.Button(win, text="EN", font=myFont, command=en, height=80, width=105)
enbutton.grid(row=1, column=2, sticky=tk.NSEW)

if __name__ == '__main__':
    threadtimeout.start()
    threadmainseries.start()
    threadseeking.start()
    win.mainloop()
    stopEN()
    stopBM()
