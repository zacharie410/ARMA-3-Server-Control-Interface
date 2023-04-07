# ARMA 3 Server Control
ARMA 3 Server Control is a Python script that simplifies the process of managing an ARMA 3 server by automating common tasks and providing a graphical interface for easy server management.

![ARMA 3 SERVER CONTROL INTERFACE](https://repository-images.githubusercontent.com/613191486/77209a21-3028-4626-9789-eb506c8fb03d)

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
