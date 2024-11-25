import subprocess
import sys
import time

command = [
            "open", "-na", "Google Chrome", "--args", "--profile-directory=" + "Profile 3"
        ]
    
# Run the command
subprocess.run(command, check=True)

time.sleep(3)

script = """
        tell application "Google Chrome"
            quit
        end tell
        """
subprocess.run(["osascript", "-e", script], check=True)
print("Google Chrome closed.")