import subprocess
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

def adjust_process_volume(fname, volume_level):
    output = subprocess.check_output(('TASKLIST', '/FO', 'CSV')).decode()
    output = output.replace('"', '').split('\r\n')
    header = output[0].split(',')  
    process_data = [i.split(',') for i in output[1:] if i]

    process_dict = {i[0]: dict(zip(header[1:], i[1:])) for i in process_data}

    for name, _ in sorted(process_dict.items(), key=lambda x: x[0].lower()):
        process_name = name.lower()
        if fname in process_name or "all" in fname:
            session_name = name.replace(".exe", "")
            sessions = AudioUtilities.GetAllSessions()

            for session in sessions:
                volume_control = session._ctl.QueryInterface(ISimpleAudioVolume)
                
                if session.Process and session.Process.name() == f"{session_name}.exe":
                    volume_control.SetMasterVolume(volume_level, None) 
                    print(f"Set volume for {session_name}: {volume_control.GetMasterVolume()}")


def adjust_all_process_volume(volume_level):
    adjust_process_volume("all", volume_level)

