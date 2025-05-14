# Import required libraries
from flask import Flask, request, send_file  # Flask web server & file response
import pyautogui as pag                      # For simulating key presses, screenshots
import subprocess                            # For running system commands
import threading                             # For background tasks like keylogger
import os                                    # OS-level operations like path and system calls
import time                                  # Sleep or delays if needed
import smtplib                               # Sending emails (used in some extensions)
import webbrowser as web                     # Open URLs in default browser
import psutil                                # Battery info and system stats
import win32gui, win32con                    # Windows GUI operations (hiding console)
import cv2                                   # Webcam usage
from email.mime.image import MIMEImage       # Email image attachments
from email.mime.multipart import MIMEMultipart
import socket                                # Network operations (getting IP address)
import subprocess                            # For executing system commands
import pyqrcode                              # QR code generation
import png                                    # PNG image handling (for QR codes)
# # Import your custom modules (must be defined separately)
import osi       # Command conditioning logic
import vol       # Volume control logic
import voice     # Text-to-speech module
# from logger import logger  # Keylogger function
# from hostname import hostname  # Computer hostname (like 'Sushant-PC')

def encryp(method, message):
    
    source_chars = "123ABCDEFGHIJ4567890KLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz~!@#$%^&*()_-+=[];',|:<>."
    target_chars = "<IemS)_9^DxXd6Z3|fVp8aF&2'~-5$k[QWP(*w?,>%KqCilOYT]MsJ!:u=tGvRoH4ghj+10U@zcAbE;7nrLy#NB"

    
    if method == "enc":
        from_chars = source_chars
        to_chars = target_chars
    elif method == "dec":
        from_chars = target_chars
        to_chars = source_chars
    else:
        raise ValueError("Method must be 'enc' for encryption or 'dec' for decryption")

    words = message.split(" ")
    transformed_words = []

    for word in words:
        transformed_word = ""
        for char in word:
            if char in from_chars:
                index = from_chars.index(char)
                transformed_word += to_chars[index]
            else:
                
                transformed_word += char
        transformed_words.append(transformed_word)

    result = " ".join(transformed_words)
    return result

# Flag for video (used elsewhere in the program, currently set to 0)
video_flag = 0

# Get the hostname of the current machine
hostname = socket.gethostname()

# Get the IP address associated with the hostname
ip_from_hostname = socket.gethostbyname(hostname)

# Convert the IP address to string (just in case)
ip_from_hostname = str(ip_from_hostname)

# Create a UDP socket to determine the local IP used for internet connection
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Connect to a public DNS server (Google DNS at 8.8.8.8) to get the outbound IP
s.connect(("8.8.8.8", 80))

# Get the local IP address assigned to the network interface used to reach 8.8.8.8
local_ip = s.getsockname()[0]

# Close the socket after use
s.close()

hostname = socket.gethostname()
ip_from_hostname = str(socket.gethostbyname(hostname))

# More reliable method to get LAN IP


url_string = f"http://{local_ip}:5000/"
qr_code = pyqrcode.create(url_string)
qr_code.png("qrcode.png", scale=6)

# Initialize Flask app
app = Flask(__name__)

# Function to handle and execute commands
def process_command(text: str):
    text = text.lower()                    # Normalize input
    original_text = text                   # Keep original for fallback
    processed_text = "Unknown command."    # Default response

    def respond(msg):
        return msg % hostname              # Inject hostname into responses

    def replace_and_trim(cmd):
        return text.replace(f"{cmd} ", "") # Trim command prefix

    # Command: !unmute <target>
    if osi.conditioner(1, text, "!unmute", 1) == "true":
        target = replace_and_trim("!unmute")
        vol.v(target, 1)  # Unmute using volume module
        return f"'{target}' unmuted! on {hostname} computer!"

    # Command: !mute <target>
    elif osi.conditioner(1, text, "!mute", 1) == "true":
        target = replace_and_trim("!mute")
        vol.v(target, 0)  # Mute using volume module
        return f"'{target}' muted! on {hostname} computer!"

    # Command: !lock
    elif osi.conditioner(1, text, "!lock", 1) == "true":
        subprocess.call('rundll32.exe user32.dll, LockWorkStation')
        return respond("%s computer is locked now!")

    # Command: !sleep
    elif osi.conditioner(1, text, "!sleep", 1) == "true":
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return respond("""%s computer going to sleep.\nThank you for using Entropy!\n\npowered by: LominCorp""")

    # Command: !restart
    elif osi.conditioner(1, text, "!restart", 1) == "true":
        subprocess.call(["shutdown", "/r"])
        return respond("""Restarting %s computer.\nThank you for using Entropy!\n\npowered by: LominCorp""")

    # Command: !shutdown
    elif osi.conditioner(1, text, "!shutdown", 1) == "true":
        subprocess.call(["shutdown", "/s"])
        return respond("""Shutting down %s.\nThank you for using Entropy!\n\npowered by: LominCorp""")

    # Command: !play or !pause (toggle)
    elif osi.conditioner(1, text, "!play", 1) == "true" or osi.conditioner(1, text, "!pause", 1) == "true":
        pag.hotkey('playpause')  # Send Play/Pause key
        action = "playing" if "!play" in text else "paused"
        return respond(f"Media {action} on %s")

    # Command: !write <text>
    elif osi.conditioner(1, text, "!write", 1) == "true":
        msg = replace_and_trim("!write")
        pag.write(msg)
        return f"Typed '{msg}' on {hostname}"

    # Command: !say male <text>
    elif osi.conditioner(1, text, "!say male", 2) == "true":
        msg = replace_and_trim("!say male")
        voice.out(msg, 0, 170)  # Male voice
        return f"Saying '{msg}' in male voice on {hostname} computer"

    # Command: !say female <text>
    elif osi.conditioner(1, text, "!say female", 2) == "true":
        msg = replace_and_trim("!say female")
        voice.out(msg, 1, 170)  # Female voice
        return f"Saying '{msg}' in female voice on {hostname} computer"

    # Command: !keylogger <minutes>
    elif osi.conditioner(1, text, "!keylogger", 1) == "true":
        minutes = replace_and_trim("!keylogger")
        try:
            minutes = int(minutes)
        except:
            minutes = 1
        threading.Thread(target=logger, args=(minutes,)).start()
        return f"Keylogger initiated on {hostname}, logging keys for {minutes} minute(s)"

    # Command: !hide (hide terminal)
    elif osi.conditioner(1, text, "!hide", 1) == "true":
        hwnd = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
        return f"Console hidden on {hostname}, you will have to restart {hostname} to shutdown the server!"

    # Command: !link <url>
    elif osi.conditioner(1, text, "!link", 1) == "true":
        url = replace_and_trim("!link")
        web.open(url)
        return "DONE!"

    # Command: !screenshot
    elif osi.conditioner(1, text, "!screenshot", 1) == "true":
        path = os.getcwd()
        screenshot_path = os.path.join(path, "templates/screenshot.png")
        pag.screenshot().save(screenshot_path)
        return send_file(screenshot_path, mimetype='image/gif')

    # Command: !picture (capture from webcam)
    elif osi.conditioner(1, text, "!picture", 1) == "true":
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if ret:
            cv2.imwrite("pic.png", frame)
            cam.release()
            cv2.destroyAllWindows()
            return send_file("pic.png", mimetype='image/gif')

    # Command: !battery (battery percentage)
    elif osi.conditioner(1, text, "!battery", 1) == "true":
        battery = psutil.sensors_battery()
        return str(battery.percent)

    # Command: !close current (close current window)
    elif osi.conditioner(1, text, "!close current", 2) == "true":
        pag.hotkey('alt', 'f4')
        return respond("Current window closed on %s")

    # Command: !commands (send help image)
    elif osi.conditioner(1, text, "!commands", 1) == "true":
        return send_file("templates/commands.png", mimetype='image/gif')

    return f"'{original_text}' Unknown command!"  # Fallback for unrecognized command


# === Flask Routes (POST) ===

@app.route("/", methods=["POST"])
@app.route("/functions", methods=["POST"])
def handle_command():
    text = request.form["text"]           # Get the command from POST data
    response = process_command(text)      # Process and execute it
    return response                       # Return the result

# Run the Flask app on local server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
