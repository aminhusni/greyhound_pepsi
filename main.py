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
myFont=tkinter.font.Font(family='Helvetica',size=12,weight="bold")
serial=serial.Serial('/dev/ttyUSB0',9600)

videovar="null" #Determines the video playing

FULL=Path("/home/pi/Desktop/projectvideo/full.mp4")
player1=OMXPlayer(FULL,args=["--orientation","90","--loop","--no-osd"],dbus_name='org.mpris.MediaPlayer2.omxplayer0')


bmbutton = tk.Button(win, text="BM", font=myFont, command='', height=90, width=90)
bmbutton.grid(row=1, column=2, sticky=tk.NSEW)
enbutton = tk.Button(win, text="EN", font=myFont, command='', height=90, width=90)
enbutton.grid(row=1, column=2, sticky=tk.NSEW)


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

def mainseries():
    videovar = "language"

if __name__ == '__main__':
    win.mainloop()
