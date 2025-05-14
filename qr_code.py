import pyqrcode
import socket


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_ip = s.getsockname()[0]
s.close()

url_string = f"http://{local_ip}:5000/"
qr_code = pyqrcode.create(url_string)
qr_code.png("qrcode.png", scale=6)