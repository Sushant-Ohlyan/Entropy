import subprocess
import os

def close_application(fname):
    output = subprocess.check_output(('TASKLIST', '/FO', 'CSV')).decode()
    output = output.replace('"', '').split('\r\n')
    keys = output[0].split(',')
    proc_list = [i.split(',') for i in output[1:] if i]
    proc_dict = dict((i[0], dict(zip(keys[1:], i[1:]))) for i in proc_list)

    for name, values in sorted(proc_dict.items(), key=lambda x: x[0].lower()):
        if fname.lower() in name.lower():
            he = name.replace(".exe", "")
            os.system(f"TASKKILL /F /IM {he}.exe")


text=input("Enter the name of the application to close: ")
close_application(text)