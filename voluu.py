import subprocess
import voice
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

def adjust_process_volume(filter_str, volume_level):
    """
    Adjusts the volume of running processes that match the filter string.

    :param filter_str: A string to filter process names. Can be "all" to adjust all processes.
    :param volume_level: The volume level to set for the matching processes (0.0 to 1.0).
    """
    # Get the list of all running processes
    output = subprocess.check_output(('TASKLIST', '/FO', 'CSV')).decode()

    # Process the output to get a list of process names and their details
    output = output.replace('"', '').split('\r\n')
    header = output[0].split(',')  # Column names (e.g., process name, PID, etc.)
    process_data = [i.split(',') for i in output[1:] if i]

    # Create a dictionary with process name as the key and process details as values
    process_dict = {i[0]: dict(zip(header[1:], i[1:])) for i in process_data}

    # Loop through all processes and adjust their volume based on the filter string
    for name, _ in sorted(process_dict.items(), key=lambda x: x[0].lower()):
        process_name = name.lower()
        if filter_str in process_name or "all" in filter_str:
            # Remove ".exe" from process name for matching
            session_name = name.replace(".exe", "")
            
            # Get all audio sessions (including system processes)
            sessions = AudioUtilities.GetAllSessions()

            for session in sessions:
                volume_control = session._ctl.QueryInterface(ISimpleAudioVolume)
                
                # If the session process matches the current process, adjust the volume
                if session.Process and session.Process.name() == f"{session_name}.exe":
                    volume_control.SetMasterVolume(volume_level, None)  # Set volume
                    print(f"Set volume for {session_name}: {volume_control.GetMasterVolume()}")

def adjust_all_process_volume(volume_level):
    """
    Adjust the volume for all running processes.

    :param volume_level: The volume level to set for all processes (0.0 to 1.0).
    """
    adjust_process_volume("all", volume_level)

def announce_with_volume_adjustment(message):
    """
    Adjusts the volume, announces a message, and restores the volume.

    :param message: The message to be announced via speech.
    """
    # Lower the volume of all processes to make the announcement clear
    adjust_all_process_volume(0.2)
    
    # Use a speech synthesis function (voice.out) to announce the message
    voice.out(message)
    
    # Restore the volume back to normal after the announcement
    adjust_all_process_volume(1.0)

# Example usage of the functions
# To mute a process or adjust the volume level for a specific process:
# adjust_process_volume("chrome", 0.2)  # Lowers Chrome volume to 20%
# adjust_process_volume("all", 0.5)     # Lowers volume of all processes to 50%
