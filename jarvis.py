import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import sys
import urllib.parse
import subprocess


# ============================================================
# JARVIS - Python Voice Assistant
# Compatible with modern Python versions on Windows
# ============================================================

# -------------------- TEXT TO SPEECH -------------------------

engine = pyttsx3.init("sapi5")

voices = engine.getProperty("voices")

if voices:
    engine.setProperty("voice", voices[0].id)

engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)


def speak(text):
    """Convert text to speech."""
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()


# -------------------- GREETING -------------------------------

def wish_me():
    """Greet the user according to the current time."""

    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        greeting = "Good morning!"
    elif 12 <= hour < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"

    speak(greeting)
    speak("I am Jarvis, sir. How may I help you?")


# -------------------- SPEECH RECOGNITION ---------------------

def take_command():
    """Listen to the microphone and return recognized speech."""

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("\nListening...")

        # Adjust microphone for surrounding noise
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        recognizer.pause_threshold = 0.8

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""

    try:
        print("Recognizing...")

        query = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        print(f"You said: {query}")

        return query.lower()

    except sr.UnknownValueError:
        print("Sorry, I could not understand that.")
        speak("Sorry, I didn't understand that.")

    except sr.RequestError:
        print("Speech recognition service is unavailable.")
        speak("Speech recognition service is currently unavailable.")

    return ""


# -------------------- EMAIL FUNCTION -------------------------

def send_email(to, content):
    """
    Send email using Gmail SMTP.

    IMPORTANT:
    Store your Gmail address and App Password
    in environment variables instead of putting
    your password directly in the code.
    """

    sender_email = os.getenv("JARVIS_EMAIL")
    app_password = os.getenv("JARVIS_APP_PASSWORD")

    if not sender_email or not app_password:
        raise ValueError(
            "Email credentials are not configured. "
            "Set JARVIS_EMAIL and JARVIS_APP_PASSWORD."
        )

    with smtplib.SMTP("smtp.gmail.com", 587) as server:

        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(sender_email, app_password)

        server.sendmail(
            sender_email,
            to,
            content
        )


# -------------------- OPEN WEBSITES --------------------------

def open_website(url):
    """Open a website in the default browser."""
    webbrowser.open(url)


# -------------------- GOOGLE SEARCH --------------------------

def google_search(query):
    """Search Google for the given query."""

    query = query.strip()

    if not query:
        speak("What should I search for?")
        return

    encoded_query = urllib.parse.quote_plus(query)

    url = f"https://www.google.com/search?q={encoded_query}"

    webbrowser.open(url)

    speak(f"Searching Google for {query}")


# -------------------- WIKIPEDIA ------------------------------

def search_wikipedia(query):

    search_query = query.replace("wikipedia", "").strip()

    if not search_query:
        speak("Please tell me what you want me to search on Wikipedia.")
        return

    try:

        speak("Searching Wikipedia.")

        result = wikipedia.summary(
            search_query,
            sentences=2,
            auto_suggest=True
        )

        print("\nWikipedia:")
        print(result)

        speak("According to Wikipedia.")
        speak(result)

    except wikipedia.exceptions.DisambiguationError as e:

        print("Multiple results found:")
        print(e.options[:5])

        speak(
            "There are multiple results for that topic. "
            "Please be more specific."
        )

    except wikipedia.exceptions.PageError:

        speak("I could not find that page on Wikipedia.")

    except Exception as e:

        print("Wikipedia error:", e)
        speak("Something went wrong while searching Wikipedia.")


# -------------------- APPLICATIONS ---------------------------

def open_application(application):

    try:

        if application == "vscode":

            paths = [
                r"C:\Users\dell\AppData\Local\Programs\Microsoft VS Code\Code.exe",
                r"C:\Program Files\Microsoft VS Code\Code.exe"
            ]

            for path in paths:

                if os.path.exists(path):
                    os.startfile(path)
                    return

            speak("I could not find Visual Studio Code.")

        elif application == "chrome":

            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ]
            for path in chrome_paths:
                if os.path.exists(path):
                    os.startfile(path)
                    return
            speak("I could not find Google Chrome.")
    except Exception as e:
        print("Application error:", e)
        speak("I could not open that application.")
# -------------------- NOTES ----------------------------------
def take_note():
    speak("What should I write down?")

    note = take_command()

    if not note:
        speak("I didn't hear the note.")
        return
    filename = "jarvis_notes.txt"
    timestamp = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    with open(filename, "a", encoding="utf-8") as file:

        file.write(
            f"[{timestamp}] {note}\n"
        )
    speak("Your note has been saved.")
# -------------------- MAIN PROGRAM ---------------------------
if __name__ == "__main__":

    wish_me()

    while True:

        query = take_command()
        if not query:
            continue;
        # ======================================================
        # WIKIPEDIA
        # ======================================================
        if "wikipedia" in query:
            search_wikipedia(query)
        # ======================================================
        # YOUTUBE
        # ======================================================
        elif "open youtube" in query:
            speak("Opening YouTube.")
            open_website("https://www.youtube.com")
        # ======================================================
        # GOOGLE
        # ======================================================
        elif "open google" in query:
            speak("Opening Google.")
            open_website("https://www.google.com")
        # ======================================================
        # GITHUB
        # ======================================================
        elif "open github" in query:
            speak("Opening GitHub.")
            open_website("https://github.com")
        # ======================================================
        # STACK OVERFLOW
        # ======================================================
        elif "open stackoverflow" in query or "open stack overflow" in query:
            speak("Opening Stack Overflow.")
            open_website("https://stackoverflow.com")
        # ======================================================
        # LINKEDIN
        # ======================================================
        elif "open linkedin" in query:
            speak("Opening LinkedIn.")
            open_website("https://www.linkedin.com")
        # ======================================================
        # GOOGLE SEARCH
        # ======================================================
        elif query.startswith("search for"):
            search_text = query.replace("search for", "", 1)
            google_search(search_text)
        elif query.startswith("google"):
            search_text = query.replace("google", "", 1)
            google_search(search_text)
        # ======================================================
        # TIME
        # ======================================================
        elif "the time" in query or query == "time":
            current_time = datetime.datetime.now().strftime(
                "%I:%M %p"
            )
            speak(f"Sir, the time is {current_time}.")
        # ======================================================
        # DATE
        # ======================================================
        elif "today's date" in query or "what is the date" in query:
            current_date = datetime.datetime.now().strftime(
                "%d %B %Y"
            )
            speak(f"Today's date is {current_date}.")
        # ======================================================
        # OPEN VS CODE
        # ======================================================
        elif "open code" in query or "open vs code" in query:
            speak("Opening Visual Studio Code.")
            open_application("vscode")
        # ======================================================
        # OPEN CHROME
        # ======================================================
        elif "open chrome" in query:
            speak("Opening Google Chrome.")
            open_application("chrome")
        # ======================================================
        # TAKE NOTE
        # ======================================================
        elif "take a note" in query or "write a note" in query:
            take_note()
        # ======================================================
        # EMAIL
        # ======================================================
        elif "email to aryan" in query:
            try:
                speak("What should I say?")
                content = take_command()
                if not content:
                    speak("I could not understand the email.")
                    continue
                to = "aryanssharma1605@gmail.com"
                send_email(to, content)

                speak("Email has been sent successfully.")

            except Exception as e:

                print("Email error:", e)

                speak(
                    "Sorry sir, I was unable to send the email."
                )
        # ======================================================
        # SHUTDOWN JARVIS
        # ======================================================
        elif (
            "exit" in query
            or "quit" in query
            or "stop jarvis" in query
            or "goodbye" in query
        ):
            speak("Goodbye sir. Have a great day!")
            sys.exit()
        # ======================================================
        # UNKNOWN COMMAND
        # ======================================================
        else:
            speak(
                "I don't have a command for that yet."
            )
