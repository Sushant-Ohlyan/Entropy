import socket

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
