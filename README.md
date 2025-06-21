
# 🤖 Voice Assistant JARVIS using Python

This is a simple **voice assistant project in Python** that uses speech recognition, web browsing, music playback, news fetching, and AI interaction using **Gemini API**.

## 🛠️ Features

- 🗣️ Wake-word Detection ("Jarvis")
- 🌐 Open websites like Google, YouTube, Facebook, etc.
- 🎵 Play songs from a custom music library
- 📰 Read latest news headlines (using NewsAPI)
- 🤖 Respond to general queries using Google Gemini API (like ChatGPT)
- 🗣️ Text-to-speech using gTTS and pyttsx3

---

## ✅ Prerequisites

Install Python (>= 3.7)

## 📦 Installation

Run the following commands in your terminal:

```bash
pip install SpeechRecognition
pip install pyttsx3
pip install pygame
pip install gTTS
pip install requests
pip install python-dotenv
pip install google-generativeai
```

Also install `PyAudio` (for microphone access):

```bash
pip install pipwin
pipwin install pyaudio
```

If `pipwin` fails, install `pyaudio` manually based on your Python version and OS.

---

## 🔑 Setup

1. Create a file named `.env` in the same directory as your code.
2. Add your API keys inside it:

```
GEMINI_API_KEY=your_gemini_api_key_here
NEWS_API_KEY=your_newsapi_key_here
```

3. Create a Python file `musiclibrary.py` with a dictionary like:

```python
# musiclibrary.py
music = {
    "songname": "https://youtube.com/watch?v=xxxx",
    "another": "https://youtube.com/watch?v=yyyy"
}
```

---

## 🚀 Running the Assistant

Use the following command:

```bash
python main.py
```

Say "**Jarvis**" to activate it, and then speak a command.

Example commands:

- "Open Google"
- "Play [songname]"
- "News"
- "Who is Elon Musk"

---

## 🔧 Customization Tips

- 🗃️ Add more websites or voice commands in `processCommand()`.
- 🎵 Add more songs in `musiclibrary.py`.
- 🧠 Adjust Gemini prompts inside `aiProcess()` for more tailored responses.

---

## ⚠️ Notes

- Ensure your microphone is connected and working.
- Gemini API is rate-limited and may require billing setup.
- NewsAPI is free for personal use but requires an API key.

---

## 🙏 Credits

Built using:

- [Google Gemini API](https://ai.google.dev)
- [News API](https://newsapi.org)
- [gTTS](https://pypi.org/project/gTTS/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [pygame](https://www.pygame.org/news)

---

Happy Coding! 💻🎙️🧠

👨‍💻 Made with ❤️ by **Mithil**
