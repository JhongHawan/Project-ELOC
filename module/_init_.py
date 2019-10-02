from __future__ import print_function
import datetime
from pytz import timezone
import pytz
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from gtts import gTTS
import dateparser as dateparser
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
  en_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
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
    
  if 'hello' in command:
    talkToMe(
      'Hello captain, how is your day today? Pretty cool that you created me right? But it\'s time to make me smarter don\'t you think captain?')

  if 'show me a hero' in command:
    talkToMe('of course')
    url = 'https://www.youtube.com/watch?v=ryCfgtSyvoU'
    webbrowser.open(url)

def main(): 
  talkToMe('Hello captain, my name is Serina, what can I do for you today sir?')

  while True:
    assistant(myCommand())
    
  # If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    
    return service
  
def get_events(n, service):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(f'Getting the upcoming {n} events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=n, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        dt = dateparser.parse(start)
        # This dt.time() only returns the start time for the event and not the end time. 
        print(f'Event is today {dt.date()} at start time {dt.time()}', event['summary'])


service = authenticate_google()
get_events(2, service)

#TODO: Change formatting for date and have Serina tell me about the event. 