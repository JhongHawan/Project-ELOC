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
import sys

def talkToMe(command):  
  engine = pyttsx3.init()
  voices = engine.getProperty('voices')
  # for voice in voices:
  #   print("Voice:")
  #   print(" - ID: %s" % voice.id)
  #   print(" - Name: %s" % voice.name)
  #   print(" - Languages: %s" % voice.languages)
  #   print(" - Gender: %s" % voice.gender)
  #   print(" - Age: %s" % voice.age)
  en_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0"
  engine.setProperty('voice', en_voice_id)
  engine.say(command)
  engine.setProperty('volume',0.9)
  engine.runAndWait()

def myCommand(): 
  r = sr.Recognizer()
  with sr.Microphone() as source: 
    print('Prepared for next command')
    talkToMe('Prepared for your next command sir')
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
    
  if 'open peaceful lo-fi mix' in command:
    talkToMe('Aye sir, opening peace lofi mix now')
    url = 'https://www.youtube.com/watch?v=X1uaOtiJ9Vc'
    webbrowser.open(url)
    
  if 'hello' in command:
    talkToMe(
      'Hello captain, how is your day today? Pretty cool that you created me right? But it\'s time to make me smarter don\'t you think captain?')

  if 'show me a hero' in command:
    talkToMe('of course')
    url = 'https://www.youtube.com/watch?v=ryCfgtSyvoU'
    webbrowser.open(url)

  if 'storytime' in command:
    talkToMe('Certainly sir. Playing story time now.')
    url = 'https://www.youtube.com/watch?v=ni_r28ev404'
    webbrowser.open(url)

  if 'true mandalore' in command:
    talkToMe('For Mandalore sir!')
    url = 'https://www.youtube.com/watch?v=Q6QFjWcfz1c'
    webbrowser.open(url)

  if 'calendar events' in command:
    talkToMe('Of course sir.')
    # get the exact number of entries the person wants. 
    # Or just ask them for the day they want the information for. 
    get_events(2, service)
    
  if 'iron man workshop' in command:
    talkToMe('For Mandalore sir!')
    url = 'https://www.youtube.com/watch?v=BN1WwnEDWAM'
    webbrowser.open(url)
    
  if 'ac dc mix' in command: 
    talkToMe('Playing AC DC mix now')
    url = 'https://www.youtube.com/watch?v=zFgNyCItmcE&list=PLxAOpDAvaMej0t20MTfd4bOEtRqwmL26R'
    webbrowser.open(url)
    
  # For some reason it still exits here even though you don't tell it to tshut down. 
  if 'shut down' or 'quit' or 'exit' or 'terminate' or 'power down' or 'power off' in command:
    talkToMe('Powering down now sir. Have a lovely day.')
    sys.exit()
  
def main(): 
  talkToMe('Welcome home sir, how may I serve you?')

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
    print(f'Getting the upcoming {n} events now sir.')
    talkToMe('Getting the upcoming ' + str(n) + ' events now sir.')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=n, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        talkToMe('No upcoming events found.')
    for event in events:
        # {Y} days ago, yesterday, today, tomorrow, in {X} days
        dateDiff = 'today'
        today = datetime.date.today()
        start = event['start'].get('dateTime', event['start'].get('date'))
        dt = dateparser.parse(start)
        time = dt.time()
        timeString = dt.time().strftime('%I:%M %p')
        date = dt.date()
        dateString = date.strftime('%A, %B %d')
        if date < today:
          dateDiff = str((today.day - date.day)) + ' days ago'
        elif date > today:
          # event is ahead of us
          dateDiff = 'in ' + str((date.day - today.day)) + ' days,'
        # This dt.time() only returns the start time for the event and not the end time. 
        print(f'Sir, event is {dateString} {dateDiff} Event begins at start time {timeString}', event['summary'])
        talkToMe('Sir, event is ' + dateString + ' ' + dateDiff + '.' + 'Event begins at start time ' + timeString + ',: ' + str(event['summary']))

service = authenticate_google()

if __name__ == "__main__":
   main()
#TODO: Change formatting for date and have Serina tell me about the event. 