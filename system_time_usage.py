import calendar
import datetime

def get_day_of_week(date_str):
    """Returns the day of the week for a given date string (dd/mm/yyyy)."""
    try:
        date_obj = datetime.datetime.strptime(date_str.replace("/", " "), '%d %m %Y')
        return calendar.day_name[date_obj.weekday()]
    except ValueError:
        return "Invalid date format"

def get_current_date():
    """Returns the current date in 'day month year' format."""
    now = datetime.datetime.now()
    return '%s %s %s' % (now.day, now.month, now.year)

def get_current_time(mode="all"):
    """Returns the current time based on the mode ('all', 'hour', 'min', 'sec')."""
    now = datetime.datetime.now()
    if mode == "all":
        return "%s:%s:%s" % (now.hour, now.minute, now.second)
    elif mode == "hour":
        return now.hour
    elif mode == "min":
        return now.minute
    elif mode == "sec":
        return now.second
    else:
        return "Invalid time mode"

def get_current_day():
    """Returns the current day of the week."""
    return get_day_of_week(get_current_date())

# Command list (help text)
help_text = """
Commands:
0. !close  <appname>   (Close the app)
1. !open   <appname>   (Open the app)
2. !screenshot         (Take a screenshot of the screen)
3. !vl     <appname>   (Set the volume of the app to low)
4. !vm     <appname>   (Set the volume of the app to medium)
5. !vf     <appname>   (Set the volume of the app to full)
6. !vr                 (Reset volume of all apps to normal)
7. !mute   <appname>   (Mute the volume of the app)
8. !unmute <appname>   (Unmute the app)
9. !play               (Play paused media)
10. !pause             (Pause media)
11. !lock              (Lock the computer)
12. !say female <text> (Say text with a female voice)
13. !say male <text>   (Say text with a male voice)
14. !hide              (Hide the program window)
15. !s <search_term>   (Search for term on Google)
16. !write <text>      (Type text)
17. !keylogger <minutes> (Log keystrokes for given minutes)
18. !sleep             (Put computer to sleep)
19. !restart           (Restart the computer)
20. !shutdown          (Shutdown the computer)
21. !fix               (Try to fix an unresponsive system)
22. !link <url>        (Open the link in browser)
23. !close current     (Close the current window or app)
24. !picture           (Take a picture from the webcam)
"""

# Example usage of the functions:
if __name__ == "__main__":
    print("Current Day:", get_current_day())  # Current day
    print("Current Time (hh:mm:ss):", get_current_time())  # Current time in 'hh:mm:ss'
    print("Current Hour:", get_current_time("hour"))  # Current hour
    print("Help Text:", help_text)  # Display available commands
