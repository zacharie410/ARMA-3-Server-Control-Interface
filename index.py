import os
import subprocess
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from pathlib import Path
import shutil
import datetime

def get_server_dir():
    # Find the Steam installation directory from the registry
    steam_dir = None
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam") as key:
            steam_dir = winreg.QueryValueEx(key, "InstallPath")[0]
    except Exception:
        pass

    if steam_dir is None:
        steam_dir = input("Unable to find Steam installation directory. Please enter the path manually: ")

    # Find the ARMA 3 Dedicated Server folder
    server_dir = os.path.join(steam_dir, "steamapps", "common", "Arma 3 Server")
    if not os.path.exists(server_dir):
        print("Unable to find ARMA 3 Dedicated Server directory. Please enter the path manually.")
        server_dir = input("ARMA 3 Dedicated Server path: ")

    return server_dir

def get_workshop_dir():
    # Find the Steam installation directory from the registry
    steam_dir = None
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam") as key:
            steam_dir = winreg.QueryValueEx(key, "InstallPath")[0]
    except Exception:
        pass

    if steam_dir is None:
        steam_dir = input("Unable to find Steam installation directory. Please enter the path manually: ")

    # Find the ARMA 3 installation folder
    arma_dir = os.path.join(steam_dir, "steamapps", "common", "Arma 3")
    if not os.path.exists(arma_dir):
        print("Unable to find ARMA 3 installation directory. Please enter the path manually.")
        arma_dir = input("ARMA 3 installation path: ")

    # Find the !Workshop folder inside the ARMA 3 installation folder
    workshop_dir = os.path.join(arma_dir, "!Workshop")
    if not os.path.exists(workshop_dir):
        print("Unable to find ARMA 3 Workshop directory. Please enter the path manually.")
        workshop_dir = input("ARMA 3 Workshop path: ")

    return workshop_dir



def update_mod_keys(keys_dir, mod_dirs, server_params):
    # clear all .bikey files from the keys folder
    print('Clearing old .bikey files from the keys folder...')
    for file in Path(keys_dir).glob('*.bikey'):
        if file.name != 'a3.bikey':
            file.unlink()

    print('Updating mod keys...' + mod_dirs[0])
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

def start_server(keys_dir, mod_dirs, server_params):
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
    args = [server_exe] + server_params + ['-mod=' + ';'.join(mods)]

    # Start the server process
    subprocess.Popen(args, creationflags=subprocess.CREATE_NEW_CONSOLE)

    
def stop_server():
    subprocess.run(['taskkill', '/f', '/im', 'arma3server_x64.exe'])
    print('Server stopped.')

# GUIDE
with open('params_help_guide.txt', 'r') as file:
    PARAMS_HELP_GUIDE = file.read()

# Set up the default server directory and mod directories


if not os.path.exists('profiles'):
    os.makedirs('profiles')

# Function to create the main menu
def edit_profile_and_destroy_main(profile_name, main_window):
    # Destroy the main menu window
    main_window.destroy()
    create_profile_edit(profile_name)

    # Function to create the main menu
def return_to_menu(profile_window):
    # Destroy the main menu window
    profile_window.destroy()
    create_main_menu()


def create_main_menu():
    main_window = tk.Tk()
    # Create the main window
    icon_image = Image.open('./app_icon.png')
    tk_icon = ImageTk.PhotoImage(icon_image)


    main_window.wm_iconphoto(True, tk_icon)
    main_window.title('ARMA 3 Server Control')
    main_window.geometry('600x400')
    main_window.configure(bg='#383838')

    # Create the header label
    header_label = tk.Label(main_window, text='Server Profile', font=('Arial', 18), fg='#FFFFFF', bg='#383838')
    header_label.pack(pady=10)

    # Create the profile selection dropdown menu
    profile_options = ['Profile 1', 'Profile 2', 'Profile 3'] # Replace with actual profiles
    selected_profile = tk.StringVar()
    selected_profile.set(profile_options[0])
    profile_menu = tk.OptionMenu(main_window, selected_profile, *profile_options)
    profile_menu.configure(font=('Arial', 12), bg='#4F4F4F', fg='#FFFFFF', activebackground='#808080', activeforeground='#FFFFFF', highlightthickness=0)
    profile_menu.pack(pady=10)

    # Create the profile edit button
    edit_button = tk.Button(main_window, text='Edit Profile', font=('Arial', 12), bg='#4F4F4F', fg='#FFFFFF', activebackground='#808080', activeforeground='#FFFFFF', highlightthickness=0, command=lambda: edit_profile_and_destroy_main(selected_profile.get(), main_window))
    edit_button.pack(pady=10)

    main_window.mainloop()

def create_profile_edit(profile_name):
    load_profile(profile_name)
    print(f'Loading profile: {profile_name}')
    print(f'Server directory: {server_dir}')
    print(f'Keys directory: {keys_dir}')
    print(f'Mod directories: {mod_dirs}')
    print(f'Server parameters: {server_params}')
    # Create the profile edit window
    profile_window = tk.Tk()
    profile_window.title(f'{profile_name} Profile Editor')
    profile_window.geometry('800x720')

    # Create the header frame
    header_frame = tk.Frame(profile_window, bg='#2C3E50')
    header_frame.pack(fill=tk.X)

    # Create the header label
    header_label = tk.Label(header_frame, text=f'{profile_name} Profile Editor', font=('Helvetica', 20), 
                            bg='#2C3E50', fg='white', padx=10)
    header_label.pack(side=tk.LEFT)

    # Create the server directory frame
    server_dir_frame = tk.Frame(profile_window)
    server_dir_frame.pack(pady=20)

    # Create the server directory label
    server_dir_label = tk.Label(server_dir_frame, text='Server Directory:', font=('Helvetica', 14))
    server_dir_label.pack(side=tk.LEFT)

    # Create the server directory input field
    server_dir_input = tk.Entry(server_dir_frame, width=40)
    server_dir_input.pack(side=tk.LEFT, padx=10)
    server_dir_input.insert(tk.END, server_dir)

    # Create the server directory browse button
    server_dir_button = tk.Button(server_dir_frame, text='Browse', font=('Helvetica', 14), 
                                  command=lambda: browse_for_server_dir(server_dir_input))
    server_dir_button.pack(side=tk.LEFT)

    # Create the mod directory frame
    mod_dirs_frame = tk.Frame(profile_window)
    mod_dirs_frame.pack(pady=20)

    # Create the mod directory label
    mod_dirs_label = tk.Label(mod_dirs_frame, text='Mod Directories:', font=('Helvetica', 14))
    mod_dirs_label.pack(side=tk.LEFT)

    # Create the mod directory input field
    mod_dirs_input = tk.Entry(mod_dirs_frame, width=40)
    mod_dirs_input.pack(side=tk.LEFT, padx=10)
    mod_dirs_input.insert(tk.END, mod_dirs)

    # Create the mod directory browse button
    mod_dirs_button = tk.Button(mod_dirs_frame, text='Browse', font=('Helvetica', 14), 
                                 command=lambda: browse_for_mod_dirs(mod_dirs_input))
    mod_dirs_button.pack(side=tk.LEFT)

    # Create the server parameters frame
    params_frame = tk.Frame(profile_window)
    params_frame.pack(side=tk.TOP, pady=10)

    # Create the server parameters label
    params_label = tk.Label(params_frame, text='Server Parameters:', font=('Helvetica', 14))
    params_label.pack(side=tk.TOP)

    # Create the server parameters text field
    params_text = tk.Text(params_frame, width=50, height=5, font=('Helvetica', 12))
    params_text.pack(side=tk.TOP, padx=10)

    # Set the default server parameters in the text field
    params_text.insert(tk.END, server_params)

    # Create the select parameter frame
    select_param_frame = tk.Frame(params_frame)
    select_param_frame.pack(side=tk.TOP)

    # Create the default parameter text
    default_param = tk.StringVar(profile_window, 'Select a parameter...')

    # Create the server parameters options menu
    params_options = ['-profiles', '-config', '-serverMod', '-world', '-name', '-cfg', '-autoinit',
                    '-nologs', '-nosplash', '-noFilePatching', '-noSound', '-enableHT', '-hugePages', '-malloc',
                    '-maxMem=3072', '-maxVRAM=2047', '-noPause', '-noPauseMP', '-exThreads=7', '-filePatching', '-port=2302',
                    '-password=', '-loadMissionToMemory',
                    '-ip=127.0.0.1', '-rankings', '-serverLog', '-netlog',
                    '-h', '-help', '-?', '-showScriptErrors', '-par', '-limitFPS=50', '-checkSignatures']

    params_menu = tk.OptionMenu(select_param_frame, default_param, *params_options, command=lambda option: insert_server_param(option, params_text))
    params_menu.configure(font=('Arial', 12), bg='#4F4F4F', fg='#FFFFFF', activebackground='#808080', activeforeground='#FFFFFF', highlightthickness=0)
    params_menu.pack(pady=5)

    # Create the server parameters help button
    params_help_button = tk.Button(params_frame, text='HELP?', font=('Helvetica', 12),
                                    command=lambda: show_params_help_guide())
    params_help_button.pack(side=tk.TOP, padx=10)


    # Function to show the parameters help guide
    def show_params_help_guide():
        # Create a new window for the guide
        guide_window = tk.Toplevel(profile_window)
        guide_window.title('Server Parameters Help Guide')
        guide_window.geometry('600x400')

        # Create a scrollable text box for the guide
        guide_text = tk.Text(guide_window, font=('Arial', 12), wrap=tk.WORD, padx=10, pady=10)
        guide_text.pack(fill=tk.BOTH, expand=True)

        # Insert the help guide text into the text box
        guide_text.insert(tk.END, PARAMS_HELP_GUIDE)
        guide_text.configure(state=tk.DISABLED)

        # Create a scrollbar for the text box
        scrollbar = tk.Scrollbar(guide_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        guide_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=guide_text.yview)

     # Create the button frame
    button_frame = tk.Frame(profile_window)
    button_frame.pack(pady=20)
    # Create the footer frame
    footer_frame = tk.Frame(profile_window)
    footer_frame.pack(pady=20)
    # Create the start button
    start_button = tk.Button(button_frame, text='Start Server', font=('Helvetica', 14), 
                             command=lambda: start_server(server_dir_input.get(), mod_dirs_input.get(), server_params))
    start_button.pack(side=tk.LEFT, padx=10)

    # Create the stop button
    stop_button = tk.Button(button_frame, text='Stop Server', font=('Helvetica', 14), command=stop_server)
    stop_button.pack(side=tk.LEFT, padx=10)

    # Create the update mod keys button
    update_button = tk.Button(button_frame, text='Update Mod Keys', font=('Helvetica', 14), 
                              command=lambda: update_mod_keys(keys_dir, mod_dirs_input.get().split(";"), server_params))
    update_button.pack(side=tk.LEFT, padx=10)

    # Create the save button
    save_button = tk.Button(footer_frame, text='Save Profile', font=('Helvetica', 14), 
                            command=lambda: save_profile(profile_name, server_dir_input, mod_dirs_input, params_text))
    save_button.pack(side=tk.LEFT, padx=10)


    # Create the back button
    menu_button = tk.Button(footer_frame, text='Select Profile', font=('Helvetica', 14), 
                            command=lambda: return_to_menu(profile_window))
    menu_button.pack(side=tk.LEFT, padx=10)

        # Create the auto-setup button
    auto_setup_button = tk.Button(profile_window, text='Auto-Setup', font=('Arial', 12), bg='#4F4F4F', fg='#FFFFFF', activebackground='#808080', activeforeground='#FFFFFF', highlightthickness=0, command=lambda: auto_setup())
    auto_setup_button.pack(pady=10)

    def auto_setup():

        # Get the ARMA 3 Dedicated Server directory
        server_dir = get_server_dir()
        workshop_dir = get_workshop_dir()
        # Set the default mod directories
        mod_dirs = [workshop_dir]

        # Set the default server parameters
        server_params = "-name=MyServer -port=2302 -password=12345 -appId=107410"

        # Update the input fields in the profile editor window
        server_dir_input.delete(0, tk.END)
        server_dir_input.insert(0, server_dir)
        mod_dirs_input.delete(0, tk.END)
        mod_dirs_input.insert(0, ';'.join(mod_dirs))
        params_text.delete('1.0', tk.END)
        params_text.insert(tk.END, server_params)

    profile_window.mainloop()

    

def insert_server_param(param, params_text):
    params_text.insert(tk.END, f' {param}')

# Function to browse for server directory
def browse_for_server_dir(server_dir_input):
    # Open the file dialog and get the selected directory
    selected_dir = filedialog.askdirectory()

    # Set the selected directory in the input field
    server_dir_input.delete(0, tk.END)
    server_dir_input.insert(0, selected_dir)

# Function to browse for mod directories
def browse_for_mod_dirs(mod_dirs_input):
    # Open the file dialog and get the selected directories
    # selected_dirs = filedialog.askdirectory()
    dirselect = filedialog.Directory()
    selected_dirs = []
    while True:
        d = dirselect.show()
        if not d: break
        selected_dirs.append(d)
    # Set the selected directories in the input field
    mod_dirs_input.delete(0, tk.END)
    mod_dirs_input.insert(0, ';'.join(selected_dirs))

def save_profile(selected_profile, server_dir_input, mod_dirs_input, params_text):
    # Create the profile file path
    profile_path = f'profiles/{selected_profile}.txt'
    if os.path.exists(profile_path):
        os.remove(profile_path)
    # Write the server directory, keys directory, mod directories, and server parameters to the profile file
    with open(profile_path, 'w') as f:
        f.write(f'server_dir={server_dir_input.get()}\n')
        f.write(f'keys_dir={os.path.join(server_dir_input.get(), "keys")}\n')
        f.write(f'mod_dirs={mod_dirs_input.get()}\n')
        f.write(f'server_params={params_text.get("1.0", tk.END).strip()}\n')
    print(f'Saved profile: {selected_profile}')

def load_profile(selected_profile):
    # Create the profile file path
    profile_path = os.path.join('profiles', f'{selected_profile}.txt')

    # Read the server directory, keys directory, mod directories, and server parameters from the profile file
    if os.path.exists(profile_path):
        with open(profile_path, 'r') as f:
            for line in f:
                if line.startswith('server_dir='):
                    global server_dir
                    server_dir = line.strip().split('=')[1]
                elif line.startswith('keys_dir='):
                    global keys_dir
                    keys_dir = line.strip().split('=')[1]
                elif line.startswith('mod_dirs='):
                    global mod_dirs
                    mod_dirs = line.strip().split('=')[1]
                elif line.startswith('server_params='):
                    global server_params
                    server_params = line.replace('server_params=', '').strip().split(' ')



create_main_menu()
