from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import google.generativeai as genai
import musiclibrary
import os 
from dotenv import load_dotenv
from gtts import gTTS
import pygame
import threading
import time
app = Flask(__name__)

# Global variables for controlling the assistant
is_listening = False
assistant_thread = None

recognizer = sr.Recognizer()
engine = pyttsx3.init()
news_api_key = "c6b294eb29764f4684eeb02f8b48b121"
GEMINI_API_KEY = "AIzaSyCIj8WBTttMWnrN8o4q3U7OZH5PQKR2asE"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    try:
        tts = gTTS(text)
        tts.save("output.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("output.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
    except Exception as e:
        print(f"Error in speak function: {e}")
        # Fallback to pyttsx3 if gTTS fails
        speak_old(text)

def aiProcess(command):
    try:
        load_dotenv()
        genai.configure(api_key=GEMINI_API_KEY)
        llm = genai.GenerativeModel("gemini-1.5-flash")
        response = llm.generate_content(command + " in 2 to 3 sentences")
        return response.text
    except Exception as e:
        return f"I'm sorry, I couldn't process that request. Error: {str(e)}"
        
def processCommand(c):
    response = ""
    
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
        response = "Opening Google"
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
        response = "Opening YouTube"
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
        response = "Opening Facebook"
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
        response = "Opening Instagram"
    elif "open twitter" in c.lower():
        webbrowser.open("https://twitter.com")
        response = "Opening Twitter"
    elif c.lower().startswith("play"):
        try:
            songs = c.lower().split(" ")[1]
            link = musiclibrary.music[songs]
            webbrowser.open(link)
            response = f"Playing {songs}"
        except (IndexError, KeyError):
            response = "Sorry, I couldn't find that song"
    elif "news" in c.lower():
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api_key}")
            if r.status_code == 200:
                data = r.json()
                articles = data.get("articles", [])
                response = "Here are the top news headlines:"
                for i, article in enumerate(articles[:5]):  # Limit to 5 articles
                    response += f" {i+1}. {article['title']}."
            else:
                response = "Sorry, I couldn't fetch the news right now"
        except Exception as e:
            response = f"Error fetching news: {str(e)}"
    else:
        output = aiProcess(c)
        response = output
    
    return response

def jarvis_listener():
    global is_listening
    speak("Initializing Jarvis...")
    
    while is_listening:
        r = sr.Recognizer()
        
        print("Jarvis is Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
                
            word = r.recognize_google(audio)
            print(f"Heard: {word}")
            
            if word.lower() == "jarvis":
                speak("Yes, Sir")
                with sr.Microphone() as source:
                    print("Jarvis Active....")
                    audio = r.listen(source, timeout=3)
                    command = r.recognize_google(audio)
                    print(f"Command: {command}")
                    
                    response = processCommand(command)
                    speak(response)

        except sr.WaitTimeoutError:
            pass  # Continue listening
        except sr.UnknownValueError:
            pass  # Couldn't understand audio
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)  # Brief pause before continuing

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_listening', methods=['POST'])
def start_listening():
    global is_listening, assistant_thread
    
    if not is_listening:
        is_listening = True
        assistant_thread = threading.Thread(target=jarvis_listener)
        assistant_thread.daemon = True
        assistant_thread.start()
        return jsonify({"status": "started", "message": "Jarvis is now listening"})
    else:
        return jsonify({"status": "already_running", "message": "Jarvis is already listening"})

@app.route('/stop_listening', methods=['POST'])
def stop_listening():
    global is_listening
    is_listening = False
    return jsonify({"status": "stopped", "message": "Jarvis has stopped listening"})

@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.get_json()
    command = data.get('command', '')
    
    if command:
        response = processCommand(command)
        # For web interface, we'll return the response as text instead of speaking
        return jsonify({"status": "success", "response": response})
    else:
        return jsonify({"status": "error", "message": "No command provided"})

@app.route('/speak', methods=['POST'])
def speak_text():
    data = request.get_json()
    text = data.get('text', '')
    
    if text:
        # Run speak in a separate thread to avoid blocking
        threading.Thread(target=speak, args=(text,), daemon=True).start()
        return jsonify({"status": "success", "message": "Speaking text"})
    else:
        return jsonify({"status": "error", "message": "No text provided"})

@app.route('/status')
def get_status():
    return jsonify({
        "listening": is_listening,
        "message": "Jarvis is listening" if is_listening else "Jarvis is not listening"
    })

if __name__ == '__main__':
    # Create templates folder if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    app.run(debug=True, host='0.0.0.0', port=5000)