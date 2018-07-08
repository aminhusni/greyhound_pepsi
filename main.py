import threading
import tkinter as tk
import tkinter.font
import serial
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep

win = tk.Tk()
win.title("Greyhound Pepsi")
#win.attributes("-fullscreen", True)
myFont = tkinter.font.Font(family='Helvetica',size=12,weight="bold")
arduino = serial.Serial('/dev/ttyUSB0',9600)

videovar = "null" #Determines the video playing

FULL = Path("/home/pi/Desktop/projectvideo/full.mp4")
player1 = OMXPlayer(FULL,args=["--orientation","90","--loop","--no-osd"],dbus_name='org.mpris.MediaPlayer2.omxplayer0')

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
            duration=12
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
    print("English Mode entered")
    global videovar
    attempts = 0
    videovar = "phrase1en"
    sleep(10)
    videovar = "phrase2en"
    while(True):
        print("Waiting for sound... ")
        arduino.write(b'v')
        val1 = arduino.readline()
        val2 = arduino.readline()
        total = int(val1) + int(val2)
        print("Total DETECTED was "+str(total))
        if(total >= 2):
            videovar = "dispense"
            sleep(9.5)
            arduino.write(b'd')
            sleep(1.5)
            break
        attempts += 1
        print("Attempt: "+str(attempts))
        if(attempts >= 3):
            sleep(14)
            videovar = "dispense"
            sleep(9.5)
            arduino.write(b'd')
            sleep(1.5)
            break
    attempts = 0
    mainseriesblock.set()

def bm():
    print("BM Mode entered")
    global videovar
    attempts = 0
    videovar = "phrase1bm"
    sleep(7)
    videovar = "phrase2bm"
    while(True):
        print("Waiting for sound... ")
        arduino.write(b'v')
        val1 = arduino.readline()
        val2 = arduino.readline()
        total = int(val1) + int(val2)
        print("Total DETECTED was "+str(total))
        if(total >= 2):
            videovar = "dispense"
            sleep(9.5)
            arduino.write(b'd')
            sleep(1.5)
            break
        attempts += 1
        print("Attempt: "+str(attempts))
        if(attempts >= 3):
            sleep(16)
            videovar = "dispense"
            sleep(9.5)
            arduino.write(b'd')
            sleep(1.5)
            break
    attempts = 0
    mainseriesblock.set()



mainseriesblock=threading.Event()

threadseeking = threading.Thread(target=seeking)
threadmainseries=threading.Thread(target=mainseries)

bmbutton = tk.Button(win, text="BM", font=myFont, command=bm, height=80, width=105)
bmbutton.grid(row=1, column=1, sticky=tk.NSEW)
enbutton = tk.Button(win, text="EN", font=myFont, command=en, height=80, width=105)
enbutton.grid(row=1, column=2, sticky=tk.NSEW)

if __name__ == '__main__':
    threadmainseries.start()
    threadseeking.start()
    win.mainloop()
