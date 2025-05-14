# elif(osi.conditioner(1, text, "!open", 1) == "true"):
#             text = text.replace("!open ", "")
#             try:
#                 os.system('start %s:' % text)
#             except Exception:
#                 os.system('start %s' % text)
#             processed_text = "opened '%s' on %s" % (text, hostname)
#             return processed_text

import os

folder_path = r"C:\My Documents"  # Replace with the actual path
try:
    os.startfile(folder_path)
except FileNotFoundError:
    print(f"Error: Folder not found at {folder_path}")
except Exception as e:
    print(f"An error occurred: {e}")


import subprocess

def start_application(app_name):
    try:
        if app_name.lower() == "spotify":
            subprocess.Popen(["spotify"])
            print("Spotify started.")
        
        elif app_name.lower() == "chrome":
            # You might need to adjust the path based on your Chrome installation
            subprocess.Popen(["chrome"])
            print("Chrome started.")
        
        elif app_name.lower() == "file explorer":
            subprocess.Popen(["explorer"])
            print("File Explorer started.")
        
        else:
            print(f"Application '{app_name}' not recognized.")
    
    except FileNotFoundError:
        print(f"Error: '{app_name}' executable not found. Make sure it's in your system's PATH or provide the full path.")
    
    except Exception as e:
        print(f"An error occurred while starting '{app_name}': {e}")

if __name__ == "__main__":
    while True:
        app_to_start = input("Enter the name of the application to start (Spotify, Chrome, File Explorer, or 'quit'): ").strip()
        if app_to_start.lower() == "quit":
            break
        start_application(app_to_start)