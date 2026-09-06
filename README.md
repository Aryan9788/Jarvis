🤖 JARVIS 2.0 — Python Voice Assistant

A powerful, cross-platform Python voice assistant inspired by JARVIS, capable of understanding voice commands and performing everyday computer and web-based tasks.

JARVIS 2.0 is a Python-based voice assistant that combines Speech Recognition, Text-to-Speech, Web Automation, System Control, Wikipedia Search, Notes, Email, Calculations, and Application Management into a single voice-controlled assistant.

⸻

✨ Features

🎙️ Voice Interaction

* Speech-to-text using SpeechRecognition
* Text-to-speech using pyttsx3
* Supports Indian English (en-IN)
* Dynamic microphone noise adjustment
* Natural command-based interaction

🌐 Web Automation

* Open Google
* Open YouTube
* Search Google using voice
* Search YouTube using voice
* Open GitHub
* Open LinkedIn
* Open Stack Overflow
* Search Wikipedia

💻 Computer Control

* Open Google Chrome
* Open Visual Studio Code
* Open Safari
* Open Terminal
* Open Calculator
* Open Desktop
* Open Downloads
* Open Documents

📝 Productivity

* Create notes using voice
* Read saved notes
* Timestamped notes
* System information
* Take screenshots
* Built-in help command

🧮 Utilities

* Voice calculator
* Current time
* Current date
* System information

📧 Email

* Send emails through Gmail SMTP
* Uses environment variables for credentials
* Gmail App Password support

🛡️ Reliability

* Exception handling
* Logging system
* Graceful shutdown
* Cross-platform application handling
* Secure email credential configuration

⸻

🛠️ Tech Stack

Technology	Purpose
🐍 Python	Core programming language
🎤 SpeechRecognition	Voice input
🔊 pyttsx3	Text-to-speech
📚 Wikipedia	Knowledge/search
🌐 Webbrowser	Web automation
📧 SMTP	Email functionality
💾 JSON	Data storage
📝 Logging	Error/activity tracking
💻 Subprocess	System/application control

⸻

📂 Project Structure

JARVIS/
│
├── jarvis.py
├── jarvis_notes.txt
├── jarvis_reminders.json
├── jarvis.log
├── requirements.txt
├── .gitignore
└── README.md

⸻

🚀 Installation

1. Clone the Repository

git clone https://github.com/YOUR-USERNAME/jarvis-python-assistant.git

Move into the project directory:

cd jarvis-python-assistant

⸻

2. Create a Virtual Environment

macOS / Linux

python3 -m venv venv
source venv/bin/activate

Windows

python -m venv venv
venv\Scripts\activate

⸻

3. Install Dependencies

pip install -r requirements.txt

If you haven’t created requirements.txt yet, install the packages manually:

pip install pyttsx3 SpeechRecognition wikipedia

For microphone support:

pip install PyAudio

For screenshots:

pip install pyautogui

⸻

🎤 Microphone Setup

JARVIS requires access to your computer’s microphone.

macOS

Go to:

System Settings
→ Privacy & Security
→ Microphone

Enable microphone access for:

* Terminal
* VS Code
* Python
* Your IDE

Windows

Go to:

Settings
→ Privacy & Security
→ Microphone

Enable microphone access.

⸻

▶️ Run JARVIS

Run:

python jarvis.py

On macOS/Linux you may need:

python3 jarvis.py

You should see:

╔══════════════════════════════════════════════╗
║                                              ║
║              J A R V I S  2.0               ║
║                                              ║
║          Python Voice Assistant              ║
║                                              ║
╚══════════════════════════════════════════════╝

JARVIS will then greet you and start listening for commands.

⸻

🎙️ Example Commands

🌐 Web

"Open Google"
"Open YouTube"
"Open GitHub"
"Open LinkedIn"
"Open Stack Overflow"
"Search for Python tutorials"
"Google best DSA projects"
"Search YouTube for Python projects"
"Wikipedia Albert Einstein"

💻 Applications

"Open Chrome"
"Open VS Code"
"Open Safari"
"Open Terminal"
"Open Calculator"

📁 Folders

"Open Downloads"
"Open Documents"
"Open Desktop"

📝 Notes

"Take a note"
"Write a note"
"Read my notes"

JARVIS will ask:

What should I write down?

You can respond:

Complete my DSA assignment tomorrow

The note will be saved with a timestamp.

⸻

🧮 Calculator

You can say:

"Calculate 25 plus 10"
"Calculate 100 divided by 4"
"Calculate 20 times 5"

JARVIS will respond:

The answer is 35.

⸻

🖥️ System

"System information"
"Computer information"

⸻

📸 Screenshot

"Take a screenshot"

JARVIS will create a timestamped screenshot.

Example:

jarvis_screenshot_20260906_120530.png

⸻

⏰ Date & Time

"What is the time?"
"Tell me the time"
"What's today's date?"

⸻

📧 Email

Say:

"Email to Aryan"

JARVIS will ask:

What should I say in the email?

Speak your message and JARVIS will send it through Gmail.

⸻

🔐 Email Configuration

Do not put your Gmail password directly inside the Python code.

Instead, configure environment variables.

macOS / Linux

export JARVIS_EMAIL="your-email@gmail.com"
export JARVIS_APP_PASSWORD="your-app-password"

Windows PowerShell

$env:JARVIS_EMAIL="your-email@gmail.com"
$env:JARVIS_APP_PASSWORD="your-app-password"

You should use a Gmail App Password, not your normal Gmail password.

⸻

📦 requirements.txt

Create a file named:

requirements.txt

Add:

pyttsx3
SpeechRecognition
wikipedia
PyAudio
pyautogui

Then install everything with:

pip install -r requirements.txt

⸻

🔒 Security

JARVIS follows some basic security practices:

* Email credentials are stored in environment variables.
* Credentials should never be committed to GitHub.
* .gitignore should exclude sensitive/local files.
* Calculator input is restricted to mathematical characters.
* Errors are logged instead of exposing unnecessary information.
⸻

🧠 How JARVIS Works

              ┌───────────────────┐
              │      USER         │
              │  Voice Command    │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ Speech Recognition│
              │  Speech → Text    │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ Command Processor │
              └─────────┬─────────┘
                        │
       ┌────────────────┼────────────────┐
       ▼                ▼                ▼
   Web Search       System Control     Utilities
       │                │                │
       ▼                ▼                ▼
    Google           Applications     Calculator
    YouTube          Files/Folders    Date/Time
    Wikipedia        Screenshot       System Info
       │                │                │
       └────────────────┼────────────────┘
                        ▼
              ┌───────────────────┐
              │    JARVIS TTS     │
              │    Text → Speech  │
              └───────────────────┘

⸻

🏗️ Architecture

JARVIS is organized into independent functional components:

Voice Input
     ↓
Speech Recognition
     ↓
Command Processing
     ↓
Intent Detection
     ↓
Action
     ↓
Text-to-Speech
     ↓
User

This makes it easier to add new commands and features without rewriting the entire application.

⸻

🔮 Future Improvements

The project can be expanded into JARVIS 3.0 with:

* 🧠 AI/LLM integration
* 💬 Natural language conversation
* 🌦️ Real-time weather
* 📰 News aggregation
* 📅 Calendar integration
* ⏰ Voice reminders
* 📱 WhatsApp automation
* 📂 Advanced file management
* 🔍 AI-powered web search
* 🎵 Spotify/music control
* 🖥️ Advanced system automation
* 👤 User recognition
* 🔐 Voice authentication
* 🗣️ Wake-word detection
* 🧩 Plugin architecture
* 🖥️ GUI dashboard
* 🤖 AI-powered intent detection

⸻

🎯 Project Goals

The main goal of JARVIS is to demonstrate how Python can combine:

* Voice recognition
* Artificial intelligence concepts
* Automation
* Web technologies
* Operating-system interaction
* APIs
* File handling
* Networking
* Natural language processing

into a single practical application.

⸻

📚 Learning Outcomes

Through this project, you can learn:

* Python functions and modules
* Exception handling
* File handling
* Environment variables
* Object-oriented programming concepts
* Speech recognition
* Text-to-speech systems
* Web automation
* SMTP email communication
* JSON data storage
* Regular expressions
* Subprocess management
* Cross-platform programming
* Logging and debugging

⸻
