#!/usr/bin/env python
import pdb
import subprocess
from gtts import gTTS
from audio2numpy import open_audio
import numpy as np
import sounddevice as sd
from system_hotkey import SystemHotkey
from playsound import playsound
import threading
import functools

def getClipboardData() -> str:
  p = subprocess.Popen(["xclip", "-selection", "clipboard", "-o"], stdout= subprocess.PIPE)
  retcode = p.wait()
  data = p.stdout.read()
  return data.decode("utf-8")

def setClipboardData(data: str):
    p = subprocess.Popen(['xclip','-selection','clipboard'], stdin=subprocess.PIPE)
    p.stdin.write(bytes(data, 'utf-8'))
    p.stdin.close()
    retcode = p.wait()

def createAudioFile(text: str, lang= "en-AU", filename: str= "hello.mp3"):
  tts = gTTS(text= text, lang= lang)
  tts.save(filename)

def playSoundData(filename: str= "hello.mp3"):
  t = threading.Thread(target= playsound, args=(filename,))
  t.start()
  #####
  data, samplerate = open_audio(filename)
  sd.play(data, samplerate)
  status = sd.wait()
  #####
  t.join()

def play(lang= "en", event = None):
  try:
    print("play", event)
    print("getting clipboard data")
    text = getClipboardData()
    t = threading.Thread(target= playsound, args=(f"received_{lang}.mp3",))
    t.start()
    #setClipboardData(text)
    print("calling text to speech api:", text)
    createAudioFile(text, lang)
    print("start playing")
    playSoundData()
    print("done")
    t.join()
  except:
    print("error")



if __name__ == "__main__":
  hk = SystemHotkey()
  hk.register(('alt', "shift", 'e'), callback= functools.partial(play, "en"))
  hk.register(('alt', "shift", 'a'), callback= functools.partial(play, "en-AU"))
  hk.register(('alt', "shift", 'v'), callback= functools.partial(play, "vi"))
  sd.default.device = "pulse"
  print("ready")

while True:
  pass
