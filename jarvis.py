import os
import sys
import platform
import subprocess
import webbrowser
import urllib.parse
import datetime
import smtplib
import logging
import re
import json
import random

import pyttsx3
import speech_recognition as sr
import wikipedia


# ============================================================
# JARVIS 2.0
# Advanced Python Voice Assistant
# Cross-platform: Windows / macOS / Linux
# ============================================================


# ============================================================
# CONFIGURATION
# ============================================================

APP_NAME = "JARVIS"

NOTES_FILE = "jarvis_notes.txt"
REMINDERS_FILE = "jarvis_reminders.json"
LOG_FILE = "jarvis.log"


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ============================================================
# TEXT TO SPEECH
# ============================================================

try:
    engine = pyttsx3.init()

    voices = engine.getProperty("voices")

    if voices:
        # Try to select a sensible voice
        engine.setProperty("voice", voices[0].id)

    engine.setProperty("rate", 175)
    engine.setProperty("volume", 1.0)

except Exception as e:
    engine = None
    logging.error(f"TTS initialization failed: {e}")


def speak(text):
    """
    Speak text and print it to the terminal.
    """

    print(f"\n{APP_NAME}: {text}")

    logging.info(f"JARVIS: {text}")

    if engine:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            logging.error(f"TTS error: {e}")


# ============================================================
# GREETING
# ============================================================

def wish_me():

    hour = datetime.datetime.now().hour

    if 5 <= hour < 12:
        greeting = "Good morning."
    elif 12 <= hour < 18:
        greeting = "Good afternoon."
    elif 18 <= hour < 22:
        greeting = "Good evening."
    else:
        greeting = "Hello."

    responses = [
        "How may I assist you?",
        "What can I do for you?",
        "How can I help you today?"
    ]

    speak(greeting)
    speak(f"I am Jarvis. {random.choice(responses)}")


# ============================================================
# SPEECH RECOGNITION
# ============================================================

recognizer = sr.Recognizer()

recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8


def take_command():

    try:

        with sr.Microphone() as source:

            print("\n🎤 Listening...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.4
            )

            try:

                audio = recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=10
                )

            except sr.WaitTimeoutError:

                print("No speech detected.")

                return ""

        print("🧠 Recognizing...")

        query = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        query = query.lower().strip()

        print(f"👤 You: {query}")

        logging.info(f"USER: {query}")

        return query

    except sr.UnknownValueError:

        speak("Sorry, I didn't understand that.")

    except sr.RequestError:

        speak(
            "The speech recognition service is currently unavailable."
        )

    except Exception as e:

        logging.error(f"Speech error: {e}")

        speak("There was a problem with the microphone.")

    return ""


# ============================================================
# OPEN WEBSITE
# ============================================================

def open_website(url):

    try:

        webbrowser.open(url)

    except Exception as e:

        logging.error(f"Browser error: {e}")

        speak("I could not open the website.")


# ============================================================
# GOOGLE SEARCH
# ============================================================

def google_search(query):

    query = query.strip()

    if not query:

        speak("What should I search for?")

        return

    url = (
        "https://www.google.com/search?q="
        + urllib.parse.quote_plus(query)
    )

    speak(f"Searching Google for {query}")

    open_website(url)


# ============================================================
# YOUTUBE SEARCH
# ============================================================

def youtube_search(query):

    query = query.strip()

    if not query:

        speak("What should I search for on YouTube?")

        return

    url = (
        "https://www.youtube.com/results?search_query="
        + urllib.parse.quote_plus(query)
    )

    speak(f"Searching YouTube for {query}")

    open_website(url)


# ============================================================
# WIKIPEDIA
# ============================================================

def search_wikipedia(query):

    query = re.sub(
        r"\b(search|on|wikipedia|for)\b",
        "",
        query,
        flags=re.IGNORECASE
    ).strip()

    if not query:

        speak("Please tell me what you want to search.")

        return

    try:

        speak("Searching Wikipedia.")

        result = wikipedia.summary(
            query,
            sentences=3,
            auto_suggest=True
        )

        print("\nWikipedia:")
        print(result)

        speak("According to Wikipedia.")
        speak(result)

    except wikipedia.exceptions.DisambiguationError:

        speak(
            "I found multiple results. "
            "Please be more specific."
        )

    except wikipedia.exceptions.PageError:

        speak(
            "I could not find that topic on Wikipedia."
        )

    except Exception as e:

        logging.error(f"Wikipedia error: {e}")

        speak(
            "Something went wrong while searching Wikipedia."
        )


# ============================================================
# OPEN APPLICATION
# ============================================================

def open_application(app_name):

    system = platform.system()

    try:

        # ----------------------------------------------------
        # MACOS
        # ----------------------------------------------------

        if system == "Darwin":

            apps = {
                "chrome": "Google Chrome",
                "vscode": "Visual Studio Code",
                "code": "Visual Studio Code",
                "safari": "Safari",
                "terminal": "Terminal",
                "calculator": "Calculator",
                "notes": "Notes"
            }

            app = apps.get(app_name.lower())

            if app:

                subprocess.Popen(
                    ["open", "-a", app]
                )

                speak(f"Opening {app}.")

            else:

                speak(
                    f"I don't know how to open {app_name}."
                )

        # ----------------------------------------------------
        # WINDOWS
        # ----------------------------------------------------

        elif system == "Windows":

            commands = {

                "chrome":
                    "start chrome",

                "vscode":
                    "code",

                "code":
                    "code",

                "notepad":
                    "notepad",

                "calculator":
                    "calc"
            }

            command = commands.get(
                app_name.lower()
            )

            if command:

                subprocess.Popen(
                    command,
                    shell=True
                )

                speak(f"Opening {app_name}.")

            else:

                speak(
                    f"I don't know how to open {app_name}."
                )

        # ----------------------------------------------------
        # LINUX
        # ----------------------------------------------------

        elif system == "Linux":

            commands = {

                "chrome": "google-chrome",

                "vscode": "code",

                "code": "code",

                "terminal": "gnome-terminal"
            }

            command = commands.get(
                app_name.lower()
            )

            if command:

                subprocess.Popen(
                    command,
                    shell=True
                )

                speak(f"Opening {app_name}.")

            else:

                speak(
                    f"I don't know how to open {app_name}."
                )

    except Exception as e:

        logging.error(
            f"Application error: {e}"
        )

        speak(
            f"I could not open {app_name}."
        )


# ============================================================
# NOTES
# ============================================================

def take_note():

    speak("What should I write down?")

    note = take_command()

    if not note:

        speak("I didn't hear the note.")

        return

    timestamp = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    try:

        with open(
            NOTES_FILE,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                f"[{timestamp}] {note}\n"
            )

        speak("Your note has been saved.")

    except Exception as e:

        logging.error(
            f"Note error: {e}"
        )

        speak(
            "I could not save the note."
        )


# ============================================================
# READ NOTES
# ============================================================

def read_notes():

    if not os.path.exists(NOTES_FILE):

        speak("You don't have any notes yet.")

        return

    try:

        with open(
            NOTES_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            notes = file.readlines()

        if not notes:

            speak("Your notes are empty.")

            return

        speak(
            f"You have {len(notes)} notes."
        )

        for note in notes[-5:]:

            print(note.strip())

            speak(note.strip())

    except Exception as e:

        logging.error(
            f"Read notes error: {e}"
        )

        speak(
            "I could not read your notes."
        )


# ============================================================
# SYSTEM INFORMATION
# ============================================================

def system_info():

    system = platform.system()
    version = platform.version()
    machine = platform.machine()

    speak(
        f"You are running {system} "
        f"on a {machine} computer."
    )

    print("Operating System:", system)
    print("Version:", version)
    print("Machine:", machine)


# ============================================================
# CURRENT TIME
# ============================================================

def tell_time():

    current_time = datetime.datetime.now().strftime(
        "%I:%M %p"
    )

    speak(
        f"The current time is {current_time}."
    )


# ============================================================
# CURRENT DATE
# ============================================================

def tell_date():

    current_date = datetime.datetime.now().strftime(
        "%A, %d %B %Y"
    )

    speak(
        f"Today is {current_date}."
    )


# ============================================================
# CALCULATOR
# ============================================================

def calculate(expression):

    expression = expression.lower()

    expression = expression.replace(
        "calculate",
        ""
    )

    expression = expression.replace(
        "what is",
        ""
    )

    expression = expression.strip()

    # Convert spoken operators

    expression = expression.replace(
        "plus",
        "+"
    )

    expression = expression.replace(
        "minus",
        "-"
    )

    expression = expression.replace(
        "times",
        "*"
    )

    expression = expression.replace(
        "multiplied by",
        "*"
    )

    expression = expression.replace(
        "divided by",
        "/"
    )

    expression = expression.replace(
        "power",
        "**"
    )

    # Only allow safe calculator characters

    if not re.fullmatch(
        r"[0-9+\-*/().%\s]+",
        expression
    ):

        speak(
            "I can only calculate basic mathematical expressions."
        )

        return

    try:

        result = eval(
            expression,
            {
                "__builtins__": None
            },
            {}
        )

        speak(
            f"The answer is {result}."
        )

    except Exception:

        speak(
            "I could not calculate that."
        )


# ============================================================
# OPEN FOLDER
# ============================================================

def open_folder(folder):

    system = platform.system()

    try:

        if folder == "downloads":

            path = os.path.expanduser(
                "~/Downloads"
            )

        elif folder == "documents":

            path = os.path.expanduser(
                "~/Documents"
            )

        elif folder == "desktop":

            path = os.path.expanduser(
                "~/Desktop"
            )

        else:

            speak("I don't know that folder.")

            return

        if not os.path.exists(path):

            speak(
                f"I could not find your {folder} folder."
            )

            return

        if system == "Darwin":

            subprocess.Popen(
                ["open", path]
            )

        elif system == "Windows":

            os.startfile(path)

        elif system == "Linux":

            subprocess.Popen(
                ["xdg-open", path]
            )

        speak(
            f"Opening your {folder} folder."
        )

    except Exception as e:

        logging.error(
            f"Folder error: {e}"
        )

        speak(
            "I could not open that folder."
        )


# ============================================================
# TAKE SCREENSHOT
# ============================================================

def take_screenshot():

    timestamp = datetime.datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = (
        f"jarvis_screenshot_{timestamp}.png"
    )

    try:

        if platform.system() == "Darwin":

            subprocess.run(
                [
                    "screencapture",
                    filename
                ]
            )

        elif platform.system() == "Windows":

            try:

                import pyautogui

                screenshot = pyautogui.screenshot()

                screenshot.save(filename)

            except ImportError:

                speak(
                    "Please install pyautogui first."
                )

                return

        elif platform.system() == "Linux":

            subprocess.run(
                [
                    "gnome-screenshot",
                    "-f",
                    filename
                ]
            )

        speak(
            f"Screenshot saved as {filename}."
        )

    except Exception as e:

        logging.error(
            f"Screenshot error: {e}"
        )

        speak(
            "I could not take the screenshot."
        )


# ============================================================
# SEND EMAIL
# ============================================================

def send_email(to, content):

    sender_email = os.getenv(
        "JARVIS_EMAIL"
    )

    app_password = os.getenv(
        "JARVIS_APP_PASSWORD"
    )

    if not sender_email or not app_password:

        raise ValueError(
            "Email credentials are not configured."
        )

    with smtplib.SMTP(
        "smtp.gmail.com",
        587
    ) as server:

        server.starttls()

        server.login(
            sender_email,
            app_password
        )

        server.sendmail(
            sender_email,
            to,
            content
        )


# ============================================================
# EMAIL WORKFLOW
# ============================================================

def email_aryan():

    try:

        speak("What should I say in the email?")

        content = take_command()

        if not content:

            speak(
                "I could not understand the email."
            )

            return

        recipient = "aryanssharma1605@gmail.com"

        send_email(
            recipient,
            content
        )

        speak(
            "The email has been sent successfully."
        )

    except Exception as e:

        logging.error(
            f"Email error: {e}"
        )

        speak(
            "I was unable to send the email."
        )


# ============================================================
# JARVIS HELP
# ============================================================

def show_help():

    commands = [

        "Open Google",
        "Open YouTube",
        "Open GitHub",
        "Open LinkedIn",
        "Search for Python",
        "Search YouTube for music",
        "Wikipedia Albert Einstein",
        "What is the time",
        "What is today's date",
        "Open Chrome",
        "Open VS Code",
        "Open Downloads",
        "Open Documents",
        "Take a note",
        "Read my notes",
        "Calculate 25 plus 10",
        "System information",
        "Take a screenshot",
        "Exit Jarvis"
    ]

    print("\n========== JARVIS COMMANDS ==========\n")

    for command in commands:

        print("•", command)

    print("\n=====================================\n")

    speak(
        "I have displayed the commands I currently support."
    )


# ============================================================
# MAIN COMMAND PROCESSOR
# ============================================================

def process_command(query):

    query = query.lower().strip()

    # --------------------------------------------------------
    # EXIT
    # --------------------------------------------------------

    if any(word in query for word in [
        "exit",
        "quit",
        "stop jarvis",
        "shutdown jarvis",
        "goodbye"
    ]):

        speak(
            "Goodbye sir. Have a great day."
        )

        return False

    # --------------------------------------------------------
    # HELP
    # --------------------------------------------------------

    if (
        query == "help"
        or "what can you do" in query
        or "commands" in query
    ):

        show_help()

    # --------------------------------------------------------
    # WIKIPEDIA
    # --------------------------------------------------------

    elif "wikipedia" in query:

        search_wikipedia(query)

    # --------------------------------------------------------
    # YOUTUBE SEARCH
    # --------------------------------------------------------

    elif (
        query.startswith("search youtube")
        or query.startswith("youtube search")
    ):

        search = re.sub(
            r"^(search youtube|youtube search)",
            "",
            query
        ).strip()

        youtube_search(search)

    # --------------------------------------------------------
    # YOUTUBE
    # --------------------------------------------------------

    elif "open youtube" in query:

        speak("Opening YouTube.")

        open_website(
            "https://www.youtube.com"
        )

    # --------------------------------------------------------
    # GOOGLE
    # --------------------------------------------------------

    elif "open google" in query:

        speak("Opening Google.")

        open_website(
            "https://www.google.com"
        )

    # --------------------------------------------------------
    # GITHUB
    # --------------------------------------------------------

    elif "open github" in query:

        speak("Opening GitHub.")

        open_website(
            "https://github.com"
        )

    # --------------------------------------------------------
    # LINKEDIN
    # --------------------------------------------------------

    elif "open linkedin" in query:

        speak("Opening LinkedIn.")

        open_website(
            "https://www.linkedin.com"
        )

    # --------------------------------------------------------
    # STACK OVERFLOW
    # --------------------------------------------------------

    elif (
        "open stack overflow" in query
        or "open stackoverflow" in query
    ):

        speak("Opening Stack Overflow.")

        open_website(
            "https://stackoverflow.com"
        )

    # --------------------------------------------------------
    # GOOGLE SEARCH
    # --------------------------------------------------------

    elif query.startswith("search for"):

        search_text = query[
            len("search for"):
        ].strip()

        google_search(search_text)

    elif query.startswith("google"):

        search_text = query[
            len("google"):
        ].strip()

        google_search(search_text)

    # --------------------------------------------------------
    # TIME
    # --------------------------------------------------------

    elif (
        query == "time"
        or "what is the time" in query
        or "tell me the time" in query
    ):

        tell_time()

    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

    elif (
        "today's date" in query
        or "what is the date" in query
        or "today date" in query
    ):

        tell_date()

    # --------------------------------------------------------
    # APPLICATIONS
    # --------------------------------------------------------

    elif (
        "open chrome" in query
    ):

        open_application("chrome")

    elif (
        "open vs code" in query
        or "open vscode" in query
        or "open code" in query
    ):

        open_application("vscode")

    elif "open safari" in query:

        open_application("safari")

    elif "open terminal" in query:

        open_application("terminal")

    elif "open calculator" in query:

        open_application("calculator")

    # --------------------------------------------------------
    # FOLDERS
    # --------------------------------------------------------

    elif "open downloads" in query:

        open_folder("downloads")

    elif "open documents" in query:

        open_folder("documents")

    elif "open desktop" in query:

        open_folder("desktop")

    # --------------------------------------------------------
    # NOTES
    # --------------------------------------------------------

    elif (
        "take a note" in query
        or "write a note" in query
        or "make a note" in query
    ):

        take_note()

    elif (
        "read my notes" in query
        or "show my notes" in query
    ):

        read_notes()

    # --------------------------------------------------------
    # CALCULATOR
    # --------------------------------------------------------

    elif (
        query.startswith("calculate")
        or query.startswith("what is")
        and any(
            operator in query
            for operator in [
                "plus",
                "minus",
                "times",
                "divided",
                "*",
                "/"
            ]
        )
    ):

        calculate(query)

    # --------------------------------------------------------
    # SYSTEM INFORMATION
    # --------------------------------------------------------

    elif (
        "system information" in query
        or "system info" in query
        or "computer information" in query
    ):

        system_info()

    # --------------------------------------------------------
    # SCREENSHOT
    # --------------------------------------------------------

    elif (
        "take screenshot" in query
        or "screenshot" in query
    ):

        take_screenshot()

    # --------------------------------------------------------
    # EMAIL
    # --------------------------------------------------------

    elif (
        "email to aryan" in query
        or "send email to aryan" in query
    ):

        email_aryan()

    # --------------------------------------------------------
    # GREETINGS
    # --------------------------------------------------------

    elif any(
        greeting in query
        for greeting in [
            "hello jarvis",
            "hi jarvis",
            "hey jarvis"
        ]
    );
        responses = [
            "Hello sir.",
            "Yes sir.",
            "At your service.",
            "How can I help?"
        ]
        speak(
            random.choice(responses)
        )
    # --------------------------------------------------------
    # UNKNOWN
    # --------------------------------------------------------
    else:
        speak(
            "I don't have a command for that yet. "
            "Say help to see what I can do."
        )
    return True
# ============================================================
# MAIN PROGRAM
# ============================================================
def main():
    print("""
╔══════════════════════════════════════════════╗
║                                              ║
║              J A R V I S  2.0               ║
║                                              ║
║          Python Voice Assistant              ║
║                                              ║
╚══════════════════════════════════════════════╝
""")
    logging.info("JARVIS started.")
    wish_me()
    while True:
        try:
            query = take_command()
            if not query:
                continue
            if not process_command(query):
                break
        except KeyboardInterrupt:
            speak(
                "Jarvis shutting down."
            )
            break
        except Exception as e:
            logging.exception(
                f"Unexpected error: {e}"
            )
            speak(
                "An unexpected error occurred."
            )
    logging.info("JARVIS stopped.")
# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
