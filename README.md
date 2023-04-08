# ARMA 3 Server Control
ARMA 3 Server Control is a Python script that simplifies the process of managing an ARMA 3 server by automating common tasks and providing a graphical interface for easy server management.

![ARMA 3 SERVER CONTROL INTERFACE](https://repository-images.githubusercontent.com/613191486/77209a21-3028-4626-9789-eb506c8fb03d)

### The Arma 3 Control Interface is a graphical user interface (GUI) designed to manage and control an Arma 3 dedicated server. The interface provides a user-friendly way to manage server settings, mod directories, and server parameters without the need to directly edit configuration files or use command-line tools. The key features and functionality of this Arma 3 Control Interface include:

#### Profile Management: The interface allows users to create, edit, save, and load multiple server profiles. Each profile contains server settings, mod directories, and server parameters specific to that profile.

#### Server Directory Management: Users can browse for and select the server directory, which contains the Arma 3 dedicated server installation. The interface also provides an option to open the server directory in the file explorer.

#### Mod Directory Management: Users can add and manage multiple mod directories for the server. The interface provides options to browse for mod directories and open them in the file explorer.

#### Server Parameters Management: The interface allows users to edit and manage server parameters through a text field, making it easy to customize server settings without editing configuration files directly. The interface also provides an option to insert common server parameters from a dropdown menu and a help guide that explains the function of each parameter.

#### Server Control: Users can start, stop, and update mod keys for the server directly from the interface.

#### Auto-Setup Function: The auto-setup feature automatically detects the Arma 3 dedicated server and workshop directories and sets default mod directories and server parameters for a quick and easy setup.

#### Customizable Appearance: The interface is designed with a customizable appearance, including background and text colors, making it visually appealing and easy to use.

Overall, the Arma 3 Control Interface provides a convenient and user-friendly way for server administrators to manage and control their Arma 3 dedicated server, allowing them to focus on providing a seamless gaming experience for their players.

## Features
- Simple graphical interface for easy server management
- Automatic updating of mod keys
- Support for multiple mod directories
- Saves server profile settings for easy configuration
- Start/stop server with the click of a button
## Requirements
ARMA 3 server installed on your machine
Python 3.x installed on your machine
## Installation
- Clone this repository to your local machine.
- Install requirement by running: `python install -r requirements.txt`
## Usage
- Edit the configuration file (config.json) with your desired server directory, mod directories, and startup parameters.
- Start the script by running the following command in your terminal: `python main.py`
- OR: Just run the script through your visual studio code GUI. You may need the extension for python.
- Use the graphical interface to manage your server.
## Recommended Configurations and Usage
- My config involved using my local hidden /!Workshop folder to handle my mod updates through my steam interface
- With the click of a button, you can wipe all .bikey files from your server keys directory
- the .bikey files will be replaced with the most recently updated .bikey file from the mod directory specified in config (in my case my auto updated /!Workshop mods)

# License
This project is licensed under the Apache License 2.0.

# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
