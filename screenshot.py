
from flask import Flask, render_template, send_file, redirect, url_for
import pyautogui as pag
import os

app = Flask(__name__)
screenshot_path = os.path.join('static', 'screenshot.png')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/capture')
def capture_screenshot():
    pag.screenshot().save(screenshot_path)
    return redirect(url_for('view_screenshot'))

@app.route('/view')
def view_screenshot():
    return render_template('index.html', screenshot_exists=os.path.exists(screenshot_path))

@app.route('/download')
def download_screenshot():
    if os.path.exists(screenshot_path):
        return send_file(screenshot_path, as_attachment=True)
    else:
        return "No screenshot found. Please capture first."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # accessible on LAN
