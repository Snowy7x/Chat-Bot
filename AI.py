# speech to text
import speech_recognition as sr
# search
import wikipedia
# text to speech
import pyttsx3

# Bot class
from chatterbot import ChatBot
# Trainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# Translate
from googletrans import Translator

translator = Translator()

chatBot = ChatBot(name="SnowyDragon")

#...
name = chatBot.name

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatBot)

# Train the chatbot based on the english corpus
trainer.train("chatterbot.corpus.english")

# registered speech to text
r = sr.Recognizer()

# registered text to speech
engine = pyttsx3.init()

# array / list => voices
voices = engine.getProperty('voices')

rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 10)

# default english
voiceId = 2
listenLang = 'en-US'
ara = False

engine.setProperty('voice', voices[voiceId].id)


def speak(message):
    engine.say('{}'.format(message))
    engine.runAndWait()


def listen():
    talk = "Could not get that. sorry!"
    try:
        with sr.Microphone() as source:  # use the default microphone as the audio source
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)  # listen for the first phrase and extract it into audio data
        talk = r.recognize_google(audio, language=listenLang)  # recognize speech using Google Speech Recognition
        print("Raw:" + talk)
        if ara:
            lang = translator.detect(talk).lang
            print(f"Language: {lang}")
            talk = translator.translate(talk, dest="en", src="ar").text
            print(f"eng: {talk}")
    except sr.UnknownValueError:  # speech is unintelligible
        if(ara != True):
            speak("Sorry!!, Could not understand you, Please try again!.")
        else:
            speak("المعذرة، لم استطع فهم ذلك.")
        talk = listen()
    return talk


selected = False

engine.setProperty('voice', voices[voiceId].id)

selLan = False

while not selLan:
    speak("Hey Islam")
    speak("Do you want to use Arabic?")
    answer = listen().lower()

    if "yes" in answer or "ok" in answer or "yup" in answer or "y" in answer or "i want to" in answer or "i would like" in answer:
        ara = True
        listenLang = "ar-QA"
        voiceId = 1
        engine.setProperty('voice', voices[voiceId].id)
        selLan = True
    elif "no" in answer or "nope" in answer or "nah" in answer or "n" in answer or "i do not" in answer:
        selLan = True

welcome = "Welcome back Islam!"
if ara:
    welcome = "مَرْحباً بِعودتكَ اِسلامْ"
speak(welcome)

stop = False
while not stop:
    # raw
    said = listen()

    if "exit" not in said.lower() or "stop" not in said.lower():
        print("You: " + said)
        respond = chatBot.get_response(said)
        if ara:
            respond = translator.translate(f"{respond.text}", dest="ar")
        print(f"{name}: {respond.text}")
        speak(respond.text)
    else:
        stop = True
        # Goodbye
        respond = chatBot.get_response("Goodbye")
        if ara:
            respond = translator.translate(f"{respond.text}", dest="ar")
        print(f"{name}: {respond.text}")
        speak(respond.text)