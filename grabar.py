import sounddevice as sd
import time
from scipy.io.wavfile import write,read

def countDown():
    print("Talk in three...")
    time.sleep(.2)
    print("..two")
    time.sleep(.2)
    print("..one")
    time.sleep(.2)
    print("Recording!!!")

def record(Name):
    countDown()
    fs = 48000  # Sample rate
    seconds = 2  # Duration of recording
    sd.default.device = 0

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2, dtype='float64')
    sd.wait()  # Wait until recording is finished

    write(Name, fs, myrecording)  # Save as WAV file 
    return myrecording
'''
i=11
while i<31:
    time.sleep(1)
    name = "EH"+str(i)
    print(name)
    record(name)
    i=i+1
'''