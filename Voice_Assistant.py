import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
# dictionary of names and respective email addresses
# keys and values have been removed from dictionary for privacy purposes
email_dict = {}

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("Hi I'm Zara, how can I help you?")

def takeCommand():
    # takes microphone input and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}\n")


    except Exception as e:
        print("Could you please repeat that again...")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('bahetiriya@gmail.com', 'my_password')
    server.send('bahetiriya@gmail.com', to, content)
    server.close()

if __name__ == '__main__':
    wishMe()
    while True:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            # Set number of sentences to speak from wikipedia page
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipededia")
            speak(results)
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'open my email' in query:
            webbrowser.open("gmail.com")
        elif 'play music' in query:
            music_dir = "C:\\Music\\Songs\\Favorites"
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is: {strTime}")

        # access name from dictionary
        elif 'send an email to' in query:
            try:
                speak("What should I write?")
                content = takeCommand()
                to = "recipient@domain.com"
                sendEmail(to, content)
                speak("Email has been sent")
            except Exception as e:
                speak("Unable to send email")