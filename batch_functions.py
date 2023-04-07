import subprocess
from pathlib import Path
import shutil
import os
import datetime

server_params = r"-profiles=E:\a3profiles\server -ranking=E:\rankings\ranks.log -cfg=basic.cfg -malloc=system -port=2302 -config=CONFIG_server.cfg -loadMissionToMemory -limitFPS=100"

def update_mod_keys(keys_dir, mod_dirs):
    # clear all .bikey files from the keys folder
    print('Clearing old .bikey files from the keys folder...')
    for file in Path(keys_dir).glob('*.bikey'):
        if file.name != 'a3.bikey':
            file.unlink()

    print('Updating mod keys...')
    mod_last_modified = {}
    for mods_dir in mod_dirs:
        for mod_dir in Path(mods_dir).rglob('*'):
            if mod_dir.is_dir():
                mod_dir_sanitized = ''.join(c for c in str(mod_dir) if c.isalnum() or c in '._-\\/ ')
                if mod_dir_sanitized:
                    if mod_dir_sanitized not in mod_last_modified:
                        mod_last_modified[mod_dir_sanitized] = datetime.datetime.fromtimestamp(0)
                    for file in mod_dir.glob('**/*.bikey'):
                        mod_time = os.path.getmtime(str(file))
                        mod_time_dt = datetime.datetime.fromtimestamp(mod_time)
                        if mod_time_dt > mod_last_modified[mod_dir_sanitized]:
                            mod_last_modified[mod_dir_sanitized] = mod_time_dt
                            key_file = Path(keys_dir) / file.name
                            shutil.copy(str(file), str(key_file))
                            print(f'Copied file: {file} to {key_file}')

    print('Mod keys updated.')

import os
import subprocess

def start_server(server_dir, mod_dirs):
    # Search for the server executable in the server directory
    for file in os.listdir(server_dir):
        if file.startswith('arma3server_x64'):
            server_exe = os.path.join(server_dir, file)
            break
    else:
        print('Error: arma3server_x64 executable not found in specified server directory')
        return

    # Search for mod folders in the mod directories
    mods = []
    for mod_dir in mod_dirs.split(';'):
            for mod_folder in os.listdir(mod_dir):
                if os.path.isdir(os.path.join(mod_dir, mod_folder)):
                    mods.append(os.path.join(mod_dir, mod_folder))

    # Build the command line arguments
    args = [server_exe] + server_params.split() + ['-mod=' + ';'.join(mods)]

    # Start the server process
    subprocess.Popen(args, creationflags=subprocess.CREATE_NEW_CONSOLE)

    
def stop_server():
    subprocess.run(['taskkill', '/f', '/im', 'arma3server_x64.exe'])
    print('Server stopped.')