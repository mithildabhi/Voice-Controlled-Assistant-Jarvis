import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests

recognizer = sr.Recognizer()
engine = pyttsx3.init()
news_api_key = "c6b294eb29764f4684eeb02f8b48b121"

def speak(text):
    # engine.say("I will speak this text")
    engine.say(text)
    engine.runAndWait()
    
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")    
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open twitter" in c.lower():
        webbrowser.open("https://twitter.com")
    elif c.lower().startswith("play"):
        songs = c.lower().split(" ")[1]
        link = musiclibrary.music[songs]
        webbrowser.open(link)
    
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api_key}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])
            
            for article in articles:
                speak(article["title"])
    
    else:
        # Let openai handle the rest of the commands
        pass
         
if __name__ == '__main__':
    speak("Initializing Jarvis...")
    while True:
        # Listen for the word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
        
        
        # recognize speech using Google Speech Recognition
        print("Jarvis is Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
                
            # print("You said: " + r.recognize_sphinx(audio))
            word = r.recognize_google(audio)
            if (word.lower() == "jarvis"):
                speak("Yes, Sir")
                #Listen for the word "Jarvis"
                with sr.Microphone() as source:
                    print("Jarvis Active....")
                    audio = r.listen(source, timeout= 3)
                    command = r.recognize_google(audio)
                    processCommand(command)
                    
                
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Error; {0}".format(e))