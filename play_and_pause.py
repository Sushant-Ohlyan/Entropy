import pyautogui as pag

text = input("Enter command (!play or !pause): ").strip()

if text == "!play":
    pag.hotkey('playpause')
    print("Media playing.")
elif text == "!pause":
    pag.hotkey('playpause')
    print("Media paused.")
else:
    print("Invalid command. Use !play or !pause.")

