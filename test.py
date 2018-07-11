import snowboydecoder
import sys
import signal

interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

def signalbole():
    print("detected")

model = "/home/pi/greyhound_pepsi/audio/Rasa kola hebat.pmdl"

signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.6)
print("listening")



detector.start(detected_callback=signalbole, interrupt_check=interrupt_callback, sleep_time=0.03)

detector.terminate()
