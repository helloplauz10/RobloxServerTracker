# RobloxServerTracker (MacOS Only)
A Python-based script used for notifying the information about the server's location every time you join a game in Roblox
This script doesnt read the game's memory nor it will modify it. This script will not be responsible if you get banned or not.

# Installing
```bash
$ git clone https://github.com/helloplauz10/RobloxServerTracker
$ cd RobloxServerTracker && python3 install.py
```

# Usage
The tracker will automatically launch as its embedded to Roblox already

For manual use (Neither the stdout nor the stderr will be outputed, you either have to tail the latest log that Roblox made or launch the original executable named "OldRobloxPlayer")
```bash
$ python3 /Applications/Roblox.app/Contents/MacOS/RobloxPlayer
```

# Logs
Roblox Logs and the Tracker's Logs will be saved in the same directory:
```
$HOME/Library/Logs/Roblox/
```

The Tracker's Logs will be in this format:
```
RobloxServerTracker_(Start up in epoch time).log
```

# Uninstalling
Add the option "--yes" to avoid the confirmation
```
$ python3 uninstall.py
```

# Bugs
Dont expect for the script to run in perfect condition, kindly pull an issue if you encounter an issue or a bug
### NOTE: This script might cause a memory leak due to it not detecting Roblox's closing. Open up Activity Monitor and close Python if its still running. (This rarely happens)

