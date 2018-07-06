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
            print("Relooping back to:"+str(starttime))
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
        print("From seeking thread:")
        print(videovar)

        if(videovar=="language"):
            print("video set to language")
            starttime=0
            duration=19
            player1.set_position(starttime)
            endtime=starttime+duration
            looper(starttime,"language",endtime)
    
        if(videovar=="phrase1en"):
            print("video set to phrase1en")
            starttime=11
            duration=40
            player1.set_position(starttime)
            endtime=starttime+duration
            looper(starttime,"phrase1en",endtime)


        if(videovar=="phrase1bm"):
            print("video set to phrase1bm")
            starttime=0
            duration=19
            player1.set_position(starttime)
            endtime=starttime+duration
            looper(starttime,"phrase1bm",endtime)

        if(videovar=="dispense"):
            print("video set to dispense")
            starttime=0
            duration=19
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
    global videovar
    videovar = "phrase1en"
    sleep(10)
    while(suc == 0):
        arduino.write(b'v')
        val1 = arduino.readline()
        val2 = arduino.readline()
        total = int(val1) + int(val2)
        if(total =>2):
            arduino.write(b'd')
            videovar = "dispense"
            break
        attempts =+ 1
        if(attempts == 3):
            arduino.write(b'd')
            videovar = "dispense"
    mainseriesblock.set()

def bm():
    global videovar
    videovar = "phrase1bm"
    sleep(10)
    while(suc == 0):
        arduino.write(b'v')
        val1 = arduino.readline()
        val2 = arduino.readline()
        total = int(val1) + int(val2)
        if(total =>2):
            arduino.write(b'd')
            videovar = "dispense"
            break
        attempts =+ 1
        if(attempts == 3):
            arduino.write(b'd')
            videovar = "dispense"
    mainseriesblock.set()



mainseriesblock=threading.Event()

threadseeking = threading.Thread(target=seeking)


bmbutton = tk.Button(win, text="BM", font=myFont, command=en, height=10, width=10)
bmbutton.grid(row=1, column=1, sticky=tk.NSEW)
enbutton = tk.Button(win, text="EN", font=myFont, command=bm, height=10, width=10)
enbutton.grid(row=1, column=2, sticky=tk.NSEW)

if __name__ == '__main__':
    threadseeking.start()
    win.mainloop()
