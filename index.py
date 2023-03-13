import os
import subprocess
import tkinter as tk
from tkinter import filedialog
import json

# Import the batch functions from a separate file
from batch_functions import update_mod_keys, start_server, stop_server

# Set up the default server directory and mod directories
server_dir = r'E:\a3master'
keys_dir = os.path.join(server_dir, 'keys')
mod_dirs = [r'E:\a3mods', r'D:\a3mods', r'G:\a3mods']

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
    # Create the main window
    main_window = tk.Tk()
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
    
    # Create the profile edit window
    profile_window = tk.Tk()
    profile_window.title(f'{profile_name} Profile Editor')
    profile_window.geometry('500x500')

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

    # Create the mod directory browse button
    mod_dirs_button = tk.Button(mod_dirs_frame, text='Browse', font=('Helvetica', 14), 
                                 command=lambda: browse_for_mod_dirs(mod_dirs_input))
    mod_dirs_button.pack(side=tk.LEFT)

    # Create the button frame
    button_frame = tk.Frame(profile_window)
    button_frame.pack(pady=20)
    # Create the footer frame
    footer_frame = tk.Frame(profile_window)
    footer_frame.pack(pady=20)
    # Create the start button
    start_button = tk.Button(button_frame, text='Start Server', font=('Helvetica', 14), 
                             command=lambda: start_server(server_dir_input.get(), mod_dirs_input.get()))
    start_button.pack(side=tk.LEFT, padx=10)

    # Create the stop button
    stop_button = tk.Button(button_frame, text='Stop Server', font=('Helvetica', 14), command=stop_server)
    stop_button.pack(side=tk.LEFT, padx=10)

    # Create the update mod keys button
    update_button = tk.Button(button_frame, text='Update Mod Keys', font=('Helvetica', 14), 
                              command=lambda: update_mod_keys(keys_dir, mod_dirs))
    update_button.pack(side=tk.LEFT, padx=10)

    # Create the save button
    save_button = tk.Button(footer_frame, text='Save Profile', font=('Helvetica', 14), 
                            command=lambda: save_profile(profile_name, server_dir_input, mod_dirs_input))
    save_button.pack(side=tk.LEFT, padx=10)

    # Create the back button
    menu_button = tk.Button(footer_frame, text='Select Profile', font=('Helvetica', 14), 
                            command=lambda: return_to_menu(profile_window))
    menu_button.pack(side=tk.LEFT, padx=10)

    # Set the default server directory and mod directories in the input fields
    server_dir_input.insert(0, server_dir)
    mod_dirs_input.insert(0, ';'.join(mod_dirs))

    profile_window.mainloop()


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
    
def save_profile(selected_profile, server_dir_input, mod_dirs_input):
    # Create the profile file path
    profile_path = f'profiles/{selected_profile}.txt'
    if os.path.exists(profile_path):
        os.remove(profile_path)
    # Write the server directory and mod directories to the profile file
    with open(profile_path, 'w') as f:
        f.write(f'server_dir={server_dir_input.get()}\n')
        f.write(f'mod_dirs={mod_dirs_input.get()}\n')
    print(f'Saved profile: {selected_profile}')



def load_profile(selected_profile):
    # Create the profile file path
    profile_path = os.path.join('profiles', f'{selected_profile}.txt')

    # Read the server directory and mod directories from the profile file
    if os.path.exists(profile_path):
        with open(profile_path, 'r') as f:
            for line in f:
                if line.startswith('server_dir='):
                    global server_dir
                    server_dir = line.strip().split('=')[1]
                elif line.startswith('mod_dirs='):
                    global mod_dirs
                    mod_dirs = line.strip().split('=')[1].split(';')

create_main_menu()