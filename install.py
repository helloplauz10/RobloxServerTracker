import os
import sys
import shutil
import platform
import subprocess

__version__ = "0.0.1"
robloxpath = "/Applications/Roblox.app/"
robloxexecs = os.path.join(robloxpath, "Contents/MacOs/")
robloxPlayer = os.path.join(robloxexecs, "RobloxPlayer")
oldRobloxPlayer = os.path.join(robloxexecs, "OldRobloxPlayer")
serverTracker = "servertracker.py"

def installPackage(package : str):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

if not platform.system() == "Darwin":
    print("This project is only supported and only intended to be used in MacOS")
    sys.exit()

if not os.path.exists(serverTracker):
    print("The Server Tracker script is missing!")
if os.path.exists(oldRobloxPlayer):
    print("Already Installed!")
    print("If another mod was installed in the first place, delete it first.")
    sys.exit()

# Beginning of Installation
print("Installing Roblox Server Tracker for Mac")
print(f"Version {__version__}")
if not "--yes" in sys.argv:
    shouldContinue = input("Continue? (y/n) ")
    if shouldContinue.lower() in ["n", "no", "toilet ananasdas"]:
        sys.exit()

print("Installing libraries")
installPackage("requests")
installPackage("psutil")

print("Renaming RobloxPlayer to OldRobloxPlayer")
os.rename(robloxPlayer, oldRobloxPlayer)

print("Moving the Server Tracker to Roblox and making a fake RobloxPlayer executable")
shutil.copy(serverTracker, robloxPlayer)

print("Giving perssions to fake RobloxPlayer executable")
os.chmod(robloxPlayer, 0o755) # read write execute

print("Installed successfully!")


