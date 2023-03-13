import subprocess
from pathlib import Path
import shutil
import os

server_params = r"-profiles=E:\a3profiles\server -ranking=E:\rankings\ranks.log -cfg=basic.cfg -malloc=system -port=2302 -config=CONFIG_server.cfg -loadMissionToMemory -limitFPS=100"

def update_mod_keys(keys_dir, mod_dirs):
    checked_dirs = set()
    # clear all .bikey files from the keys folder
    print('Clearing old .bikey files from the keys folder...')
    for file in Path(keys_dir).glob('*.bikey'):
        if file.name != 'a3.bikey':
            file.unlink()
    
    print('Updating mod keys...')
    for mods_dir in mod_dirs:
        for mod_dir in Path(mods_dir).rglob('*'):
            if mod_dir.is_dir() and str(mod_dir) not in checked_dirs:
                checked_dirs.add(str(mod_dir))
                for file in mod_dir.glob('*.bikey'):
                    name = file.stem[:-6].replace('@', '').replace('%', '').replace('!', '')
                    shutil.copy(str(file), str(Path(keys_dir) / (name + '.bikey')))
                    print(f'Copied file: {file} to {Path(keys_dir) / (name + ".bikey")}')
    
    print('Mod keys updated.')

def start_server(server_dir, mod_dirs):
    # Search for the server executable in the server directory
    for file in os.listdir(server_dir):
        if file.startswith('arma3server_x64'):
            server_exe = os.path.join(server_dir, file)
            break
    else:
        print('Error: arma3server_x64 executable not found in specified server directory')
        return
    
    # Build the command line arguments
    args = [server_exe] + server_params.split() + ['-mod=' + mod_dirs]
    
    # Start the server process
    subprocess.Popen(args, creationflags=subprocess.CREATE_NEW_CONSOLE)

    
def stop_server():
    subprocess.run(['taskkill', '/f', '/im', 'arma3server_x64.exe'])
    print('Server stopped.')

