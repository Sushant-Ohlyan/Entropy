from flask import Flask, request, render_template, send_file, redirect, url_for, Response, jsonify
import pyautogui as pag
import subprocess
import os
import socket
import pyqrcode
import cv2
import psutil
import time
import win32gui
import win32con
import webbrowser as web
import volume_adjutment as vol
import pyttsx3

# Flask setup
app = Flask(__name__)
screenshot_path = os.path.join('static', 'screenshot.png')

# Utilities
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

# QR code for easy access
url_string = f"http://{local_ip}:5000/"
qr_code = pyqrcode.create(url_string)
qr_code.png("static/qrcode.png", scale=6)

camera = cv2.VideoCapture(0)

def conditioner(filter_type, comparison_string, target_string, num_words):
    comparison_words = comparison_string.split(" ")
    target_words = target_string.split(" ")

    if filter_type == 1:
        start_part = " ".join(comparison_words[:num_words])
        if start_part == " ".join(target_words[:num_words]):
            return "true"
        else:
            return "false"

    elif filter_type == 2:
        count = sum(1 for word in target_words if word in comparison_words)
        return "true" if count > 0 else "false"

    elif filter_type == 3:
        end_part = " ".join(comparison_words[-num_words:])
        if end_part == " ".join(target_words[-num_words:]):
            return "true"
        else:
            return "false"

    return "false"

def close_application(fname):
    output = subprocess.check_output(('TASKLIST', '/FO', 'CSV')).decode()
    output = output.replace('"', '').split('\r\n')
    keys = output[0].split(',')
    proc_list = [i.split(',') for i in output[1:] if i]
    proc_dict = dict((i[0], dict(zip(keys[1:], i[1:]))) for i in proc_list)

    for name, values in sorted(proc_dict.items(), key=lambda x: x[0].lower()):
        if fname.lower() in name.lower():
            he = name.replace(".exe", "")
            os.system(f"TASKKILL /F /IM {he}.exe")

# Command processor
def process_command(text: str):
    text = text.lower()

    if conditioner(1, text, "!lock", 1) == "true":
        subprocess.call('rundll32.exe user32.dll,LockWorkStation')
        return "Computer locked!"

    elif conditioner(1, text, "!sleep", 1) == "true":
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Computer going to sleep."

    elif conditioner(1, text, "!restart", 1) == "true":
        subprocess.call(["shutdown", "/r"])
        return "Computer restarting..."

    elif conditioner(1, text, "!shutdown", 1) == "true":
        subprocess.call(["shutdown", "/s"])
        return "Computer shutting down..."
    
    elif conditioner(1, text, "!screenshot", 1) == "true":
        pag.screenshot().save(screenshot_path)
        return "Screenshot captured successfully.<br>" + render_template('screenshot.html')


    elif conditioner(1, text, "!battery", 1) == "true":
        battery = psutil.sensors_battery()
        if battery is None:
            return "This device does not run on a battery."
        else:
            return f"Battery is at {battery.percent}%"

    elif conditioner(1, text, "!play", 1) == "true":
        pag.hotkey('playpause')
        return "Media playing."
    
    elif conditioner(1, text, "!pause", 1) == "true":
        pag.hotkey('playpause')
        return "Media paused."

    elif conditioner(1, text, "!next", 1) == "true":
        pag.hotkey('nexttrack')
        return "Next track."
    
    elif conditioner(1, text, "!prev", 1) == "true":
        pag.hotkey('prevtrack')
        return "Previous track."
    
    elif conditioner(1, text, "!muteall",1) == "true":
        vol.adjust_all_process_volume(0.0)
        return "Muted all applications."
    
    elif conditioner(1, text, "!unmuteall", 1) == "true":
        vol.adjust_all_process_volume(1.0)
        return "Unmuted all applications."
    
    elif conditioner(1, text, "!mute", 1) == "true":
        app_name = text.replace("!mute ", "")
        vol.adjust_process_volume(app_name, 0.0)
        return f"Muted {app_name}."
    
    elif conditioner(1, text, "!unmute", 1) == "true":
        app_name = text.replace("!unmute ", "")
        vol.adjust_process_volume(app_name, 1.0)
        return f"Unmuted {app_name}."
    
    elif conditioner(1, text, "!vl",1) == "true":
        text = text.replace("!vl ", "")
        vol.adjust_process_volume(text, 0.2)
        return f"Volume set to 20% for {text}."
    
    elif conditioner(1, text, "!vm", 1) == "true":
        text = text.replace("!vm ", "")
        vol.adjust_process_volume(text, 0.5)
        return f"Volume set to 50% for {text}."
    
    elif conditioner(1, text, "!vh", 1) == "true":
        text = text.replace("!vh ", "")
        vol.adjust_process_volume(text, 0.8)
        return f"Volume set to 80% for {text}."
    
    elif conditioner(1, text, "!vmax", 1) == "true":
        text = text.replace("!vmax ", "")
        vol.adjust_process_volume(text, 1.0)
        return f"Volume set to 100% for {text}."
    
    elif conditioner(1, text, "!write", 1) == "true":
        message = text.replace("!write ", "")
        pag.write(message)
        return f"Typed '{message}'"

    elif conditioner(1, text, "!link", 1) == "true":
        url = text.replace("!link ", "")
        return url

    #search

    elif conditioner(1, text, "!search", 1) == "true":
        search_query = text.replace("!search ", "")
        web.open(f"https://www.google.com/search?q={search_query}")
        return f"Searched '{search_query}' on Google."

    #startapp
    elif conditioner(1, text, "!start", 1) == "true":
        app_name = text.replace("!start ", "")
        try:
            os.system(f'start {app_name}')
            return f"Opened {app_name}"
        except Exception:
            return f"Failed to open {app_name}"

    # fix 
    elif conditioner(1, text, "!fix", 1) == "true":
        subprocess.call('taskkill /IM explorer.exe /F', shell=True)
        time.sleep(2)
        subprocess.call(["start", "explorer.exe"], shell=True)
        return "Fixed unresponsive computer!"
    
    elif conditioner(1, text,"!hide", 1) == "true":
        hide=win32gui.GetForegroundWindow()
        win32gui.ShowWindow(hide, win32con.SW_HIDE)
        return "Console hidden! You will have to restart the server to shutdown!"

    #close
    elif conditioner(1, text, "!close current", 2) == "true":
        pag.hotkey('alt', 'f4')
        return "Closed current window!"

    elif conditioner(1, text, "!close", 1) == "true":
        app_name = text.replace("!close ", "")
        close_application(app_name)
        return f"Attempted to close {app_name}"


    else:
        return f"Unknown command: {text}"

# web cam stream
def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Routes
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        text = request.form["text"]
        result = process_command(text)
        if text.startswith("!link"):
            return render_template("link.html", url=result)
        return render_template("index.html", message=result)
    else:
        return render_template("index.html")

@app.route("/capture_screenshot")
def capture_screenshot():
    pag.screenshot().save(screenshot_path)
    return render_template("screenshot_view.html")

@app.route("/download_screenshot")
def download_screenshot():
    if os.path.exists(screenshot_path):
        return send_file(screenshot_path, as_attachment=True)
    else:
        return "Screenshot not found."

@app.route('/video')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
