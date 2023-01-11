import random
import requests
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

BASE_URL = "https://api.openweathermap.org/data/3.0/weather?"
API_KEY = "b962e5e24b5d8f4ef8bd445600d41206"


listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def get_weather(city_name):
    weather_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=imperial&APPID={API_KEY}")

    if weather_data.json()['cod'] == '404':
        return  "No City Found"
    else:
        weather = weather_data.json()['weather'][0]['main']
        description = weather_data.json()['weather'][0]['description']
        temp_fahr = weather_data.json()['main']['temp']
        temp_celc = (temp_fahr-32)*0.5556
    return f"The weather in {city_name} is: {weather}, {description} and {round(temp_celc,2)}ºC"


def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except:
        pass
    return command


def run_alexa():
    command = take_command()
    print(command)
    if 'hello' in command:
        greetings = ['Greetings', "Hello to you", 'Good to hear you!']
        rand = random.randrange(3)
        print(greetings[rand])
        talk(greetings[rand])
        print("My name is Alexa. How can i help you?")
        talk("My name is Alexa. How can i help you?")
    elif 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
    elif 'weather' in command:
        city_name = command.replace('weather in', '')
        print(get_weather(city_name))
        talk(get_weather(city_name))
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    else:
        talk('Please say the command again.')

while True:
    run_alexa()



