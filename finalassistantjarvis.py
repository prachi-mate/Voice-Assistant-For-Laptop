from gtts import gTTS
import speech_recognition as sr
import os
import re
import webbrowser
import smtplib
import requests
import win32com.client as wincl

speak = wincl.Dispatch("SAPI.SpVoice")

def talkToMe(audio):
    print(audio)
    speak.Speak(audio)

def myCommand():
    
    r = sr.Recognizer()

    with sr.Microphone() as source:
        speak_command = 'Please give some command to me...'
        talkToMe(speak_command)
        
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        talkToMe('You said: ' + command + '\n')

    except sr.UnknownValueError:
        talkToMe('Your last command couldn\'t be heard ! I can understand commands like send email, open gmail, open website xyz.com and tell me a joke')
        command = myCommand()

    return command


def assistant(command):
    message = 'Ask me to do something, I am not here for chitchat ! I can understand commands like send email, open gmail, open website xyz.com and tell me a joke'
    if 'hello' in command:
        talkToMe(message)

    elif 'hi' in command:
        talkToMe(message)

    elif 'hey' in command:
        talkToMe(message)
    
    elif 'jarvis' in command:
        talkToMe(message)

    elif 'open gmail' in command:
        #reg_ex = re.search('open gmail (.*)', command)
        url = 'https://www.gmail.com/'
        webbrowser.open(url)
        talkToMe('Done!')

    elif 'open website' in command:
        reg_ex = re.search('open website (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.' + domain
            webbrowser.open(url)
            talkToMe('Done!')
        else:
            pass

    elif 'open notepad' in command:
        os.system('notepad')
        talkToMe('Done for you!')

    elif 'whats up' in command:
        talkToMe('Just doing my thing')

    elif 'tell me a joke' in command:
        res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"}
                )
        if res.status_code == requests.codes.ok:
            talkToMe('Here is an awesome joke for you- ')
            talkToMe(str(res.json()['joke']))
        else:
            talkToMe('oops!I ran out of jokes')

    elif 'current weather in' in command:
        reg_ex = re.search('current weather in (.+)', command)
        talkToMe(reg_ex)
        if reg_ex:
            city = reg_ex.group(1)
            weather = Weather()
            location = weather.lookup_by_location(city)
            condition = location.condition()
            talkToMe('The Current weather in %s is %s The temperature is %.1f degree'
                     % (city, condition.text(), (int(condition.temp())-32)/1.8))
        else:
            talkToMe("City name not fetched")


    elif 'send email' in command:
        talkToMe('Who is the recipient?')
        recipient = myCommand()
        receiver = False

        if 'john' in recipient:
            receiver = "receiversemail"
        
        else:
            talkToMe('I am not able to fetch receiver name buddy! ')
        
        if receiver:

            talkToMe('What should I say?')
            content = myCommand()

            mail = smtplib.SMTP('smtp.gmail.com', 587)

            mail.ehlo()

            mail.starttls()

            mail.login('youremail.com', 'password')

            mail.sendmail('Testing Desktop assistant', receiver, content)

            mail.close()

            talkToMe('Email sent.')
        
        else:
            talkToMe('Buddy I am not sending email ! you failed to provide me a receiver name')
        

    elif 'bye' in command:
        talkToMe('See you later Take care !')
        exit()

    else:
            talkToMe('I don\'t know what you mean! I can understand commands like send email, open gmail, open website xyz.com and tell me a joke')

talkToMe('Hey, I am your laptop\'s Jarvis and I am ready for your command !')

while True:
    assistant(myCommand())