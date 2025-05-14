from flask import Flask, request, render_template, Response
import os
import time
import socket
import subprocess
import psutil
from subprocess import call
import smtplib
import webbrowser as web
# import osi
import cv2
import pyqrcode
import png
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
# import voice
# import vol
from flask import send_file
import pyautogui as pag
from tkinter import Tk, Label, Entry, Button
# import vact
from pynput.keyboard import Listener
import threading
import win32gui
import win32con