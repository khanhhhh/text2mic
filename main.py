#!/usr/bin/env python
import subprocess
from gtts import gTTS
from audio2numpy import open_audio
import numpy as np
import sounddevice as sd
from system_hotkey import SystemHotkey
from playsound import playsound
import threading


def getClipboardData() -> str:
  p = subprocess.Popen(["xclip", "-selection", "clipboard", "-o"], stdout= subprocess.PIPE)
  retcode = p.wait()
  data = p.stdout.read()
  return data.decode("utf-8")

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

def play(event):
  print("play", event)
  print("getting clipboard data")
  text = getClipboardData()
  print("calling text to speech api")
  createAudioFile(text)
  print("start playing")
  playSoundData()
  print("done")
  pass



if __name__ == "__main__":
  hk = SystemHotkey()
  hk.register(('alt', '1'), callback=play)
  sd.default.device = "pulse"
  print("ready")

while True:
  pass