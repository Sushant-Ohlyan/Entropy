import pyttsx3
import vol

def speak_message(message, voice_gender, speaking_rate):
    """
    Speaks the given message using the specified voice and rate.

    PARAMETERS:
    - message: The message to be spoken aloud.
    - voice_gender: The gender of the voice (0 for male, 1 for female).
    - speaking_rate: The speaking rate (words per minute).
    """
    if voice_gender == 1:
        print("Saira: ", end="")  # Female voice
    elif voice_gender == 0:
        print("David: ", end="")  # Male voice
    else:
        pass
    
    print(f"{message}\n")

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate', speaking_rate)  # Set speaking rate
    engine.setProperty('voice', voices[voice_gender].id)  # Set voice gender
    engine.say(message)  # Speak the message
    engine.runAndWait()  # Wait for the speech to finish

def speak_message_silently(message, voice_gender, speaking_rate):
    """
    Speaks the given message silently (no console output).

    PARAMETERS:
    - message: The message to be spoken aloud.
    - voice_gender: The gender of the voice (0 for male, 1 for female).
    - speaking_rate: The speaking rate (words per minute).
    """
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate', speaking_rate)  # Set speaking rate
    engine.setProperty('voice', voices[voice_gender].id)  # Set voice gender
    engine.say(message)  # Speak the message
    engine.runAndWait()  # Wait for the speech to finish



def adjust_volume_and_announce(message, voice_gender, speaking_rate):
    """
    Adjusts the volume, announces a message, and restores the volume.

    PARAMETERS:
    - message: The message to be spoken aloud.
    - voice_gender: The gender of the voice (0 for male, 1 for female).
    - speaking_rate: The speaking rate (words per minute).
    """
    vol.v("all apps", 0.2)  # Lower the volume of all applications
    speak_message(message, voice_gender, speaking_rate)  # Speak the message
    vol.v("all apps", 1.0)  # Restore the volume of all applications
