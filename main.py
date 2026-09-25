import sys
import speech_recognition as sr
import pyttsx3
import os
import psutil
import webbrowser
import pywhatkit
import wikipedia
import pyautogui
import difflib
import time
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

# ---------------- TEXT TO SPEECH ----------------
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    print("Jarvis:", text)
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        pass

# ---------------- SPEECH TO TEXT ----------------
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except:
            return ""

    try:
        command = r.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except:
        return ""

# ---------------- WAKE WORD ----------------
def wait_for_wake_word():
    print("Waiting for 'start jarvis'...")

    while True:
        command = listen()
        if "start jarvis" in command:
            speak("Yes, I am listening")
            return

# ---------------- VOLUME CONTROL ----------------
def change_volume(level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    current = volume.GetMasterVolumeLevelScalar()

    if level == "up":
        volume.SetMasterVolumeLevelScalar(min(current + 0.1, 1.0), None)
        speak("Volume increased")

    elif level == "down":
        volume.SetMasterVolumeLevelScalar(max(current - 0.1, 0.0), None)
        speak("Volume decreased")

# ---------------- CLOSE APP ----------------
def close_application(app_name):
    found = False

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            process_name = proc.info['name'].lower().replace(".exe", "")
            match = difflib.SequenceMatcher(None, app_name, process_name).ratio()

            if match > 0.6:
                proc.terminate()
                speak(f"{process_name} closed")
                found = True

        except:
            pass

    if not found:
        speak("Application not found")

# ---------------- OPEN APP ----------------
def open_application(app_name):
    speak(f"Opening {app_name}")

    try:
        os.startfile(app_name)
    except:
        pyautogui.press("win")
        time.sleep(1)
        pyautogui.write(app_name)
        time.sleep(1)
        pyautogui.press("enter")

# ---------------- COMMAND EXECUTION ----------------
def execute_command(command):

    if "exit" in command:
        speak("Bye Sir,Have a nice day")
        sys.exit()

    elif "stop jarvis" in command or "sleep" in command:
        speak("I'm going to sleep mode")
        return "sleep"

    elif command.startswith("open "):
        open_application(command.replace("open ", ""))

    elif command.startswith("close "):
        close_application(command.replace("close ", ""))

    elif "volume up" in command:
        change_volume("up")

    elif "volume down" in command:
        change_volume("down")

    elif "search" in command:
        speak("Searching")
        webbrowser.open(f"https://www.google.com/search?q={command}")

    elif "youtube" in command:
        speak("Playing on YouTube")
        pywhatkit.playonyt(command)

    elif "who is" in command or "what is" in command:
        try:
            speak(wikipedia.summary(command, sentences=2))
        except:
            speak("No results found")

    elif "type" in command:
        pyautogui.write(command.replace("type", ""), interval=0.05)

    elif "press" in command:
        pyautogui.press(command.replace("press", "").strip())

    elif "scroll down" in command:
        pyautogui.scroll(-500)

    elif "scroll up" in command:
        pyautogui.scroll(500)

    # EXTRA COMMANDS

    elif "time" in command:
        speak(time.strftime("%H:%M"))

    elif "date" in command:
        speak(time.strftime("%d %B %Y"))

    elif "battery" in command:
        speak(f"{psutil.sensors_battery().percent} percent")

    elif "screenshot" in command:
        pyautogui.screenshot("screenshot.png")
        speak("Screenshot taken")

    elif "open google" in command:
        webbrowser.open("https://google.com")

    elif "open gmail" in command:
        webbrowser.open("https://mail.google.com")

    elif "calculator" in command:
        os.startfile("calc.exe")

    elif "notepad" in command:
        os.startfile("notepad.exe")

    elif "lock" in command:
        os.system("rundll32.exe user32.dll,LockWorkStation")

    elif "shutdown" in command:
        os.system("shutdown /s /t 5")

    elif "restart" in command:
        os.system("shutdown /r /t 5")

    elif "joke" in command:
        speak("Why did the computer go to doctor? Because it has virus")

    else:
        speak("Command not recognized")

# ---------------- MAIN LOOP ----------------
def main():
    speak("Jarvis is in sleep mode")

    while True:
        wait_for_wake_word()

        while True:
            command = listen()

            if command:
                result = execute_command(command)

                if result == "sleep":
                    break

if __name__ == "__main__":
    main()