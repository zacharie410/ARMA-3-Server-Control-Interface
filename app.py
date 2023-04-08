import os
import subprocess
import json
from pathlib import Path
import shutil
import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Load the configuration from the config file
with open('config.json') as f:
    config = json.load(f)

# Set up the default server directory and mod directories
server_dir = config['server_dir']
keys_dir = os.path.join(server_dir, 'keys')
mod_dirs = config['mod_dirs']
server_params = config['start_params']

if not os.path.exists('profiles'):
    os.makedirs('profiles')

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

@app.route('/')
def index():
    profile_options = ['Server 1', 'Server 2', 'Server 3']  # Replace with actual profiles
    return render_template('index.html', profile_options=profile_options)


@app.route('/edit_profile/<profile_name>')
def edit_profile(profile_name):
    load_profile(profile_name)
    return render_template('edit_profile.html', profile_name=profile_name, server_dir=server_dir, mod_dirs=';'.join(mod_dirs))


@app.route('/save_profile', methods=['POST'])
def save_profile():
    profile_name = request.form['profile_name']
    server_dir_input = request.form['server_dir']
    mod_dirs_input = request.form['mod_dirs']

    save_profile_to_file(profile_name, server_dir_input, mod_dirs_input.split(';'))

    return redirect(url_for('index'))


@app.route('/start_server', methods=['POST'])
def start_server_route():
    server_dir_input = request.form['server_dir']
    mod_dirs_input = request.form['mod_dirs']

    start_server(server_dir_input, mod_dirs_input.split(';'))

    return "Server started", 200


@app.route('/stop_server', methods=['POST'])
def stop_server_route():
    stop_server()
    return "Server stopped", 200


@app.route('/update_mod_keys', methods=['POST'])
def update_mod_keys_route():
    mod_dirs_input = request.form['mod_dirs']

    update_mod_keys(keys_dir, mod_dirs_input.split(';'))

    return "Mod keys updated", 200

# Rest of the functions, modified to work with the web application
# ...

if __name__ == '__main__':
    app.run()
