import os
import sys

robloxpath = "/Applications/Roblox.app/"
robloxexecs = os.path.join(robloxpath, "Contents/MacOs/")
robloxPlayer = os.path.join(robloxexecs, "RobloxPlayer")
oldRobloxPlayer = os.path.join(robloxexecs, "OldRobloxPlayer")

if not "--yes" in sys.argv:
    shouldContinue = input("Would you like to uninstall it? (y/n) ")
    if shouldContinue in ["n", "no", "toilet ananasdas"]:
        sys.exit()

if not os.path.exists(oldRobloxPlayer):
    print("Is the mod already patched?")
    sys.exit()

if not os.path.exists(robloxPlayer):
    print("RobloxPlayer (patched) does not exist")
    sys.exit()
    
print("Removing patched RobloxPlayer executable")
os.remove(robloxPlayer)
        
print("Reverting OldRobloxPlayer executable back to its name")
os.rename(oldRobloxPlayer, robloxPlayer)

print("Successfully reinstalled")
