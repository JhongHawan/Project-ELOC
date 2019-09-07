from gtts import gTTS
import pyttsx3
import speech_recognition as sr
import os
import webbrowser
import smtplib

def talkToMe(command):  
  engine = pyttsx3.init()
  voices = engine.getProperty('voices')
  for voice in voices:
    print("Voice:")
    print(" - ID: %s" % voice.id)
    print(" - Name: %s" % voice.name)
    print(" - Languages: %s" % voice.languages)
    print(" - Gender: %s" % voice.gender)
    print(" - Age: %s" % voice.age)
  en_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0"
  engine.setProperty('voice', en_voice_id)
  engine.say(command)
  engine.setProperty('volume',0.9)
  engine.runAndWait()

def myCommand(): 
  r = sr.Recognizer()
  with sr.Microphone() as source: 
    print('Prepared for next command')
    r.pause_threshold = 1
    r.adjust_for_ambient_noise(source, duration = 1)
    audio = r.listen(source)

  try: 
    command = r.recognize_google(audio)
    print('Command given: ' + command + '/n')

  except sr.UnknownValueError:
    assistant(myCommand())
    
  return command 

def assistant(command):
  command = command.lower()
  if 'open programming mix' in command: 
    talkToMe('Opening the programming mix sir')
    url = 'https://www.youtube.com/watch?v=l9nh1l8ZIJQ'
    webbrowser.open(url)
    
  if 'open asian lo-fi mix' in command:
    talkToMe('Aye sir, opening asian lofi mix now')
    url = 'https://www.youtube.com/watch?v=X1uaOtiJ9Vc'
    webbrowser.open(url)
    
  if 'hi' in command: 
    talkToMe(
      'Hello captain, how is your day today? Pretty cool that you created me right? But it\'s time to make me smarter don\'t you think captain?')

talkToMe('Hello captain, my name is Eba, what can I do for you today sir?')

while True:
  assistant(myCommand())