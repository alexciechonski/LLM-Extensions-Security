import subprocess
import time
import signal
import os
from playwright.sync_api import sync_playwright

def start_chrome(profile_num):
    command = [
            "open", "-na", "Google Chrome", "--args", "--profile-directory=" + f"Profile {profile_num}"
        ]
    subprocess.run(command, check=True)
    print(f"Chrome Profile {profile_num} instance opened.")

def close_chrome():
    # script = """
    #     tell application "Google Chrome"
    #         quit
    #     end tell
    #     """
    # subprocess.run(["osascript", "-e", script], check=True)
    # print("Google Chrome closed.")
    subprocess.run(["killall", "Google Chrome"], check=True)


def mitm(output_file):
    mitmweb_command = [
        "mitmproxy",
        "--save-stream-file", output_file
    ]
    mitmweb_process = subprocess.Popen(mitmweb_command)
    return mitmweb_process

def close_mitm(process):
    os.kill(process.pid, signal.SIGTERM)

def accept_buttons():
    pass

def automate(output_file, i):
        start_chrome(i+4)
        process = mitm(output_file)
        time.sleep(10)
        close_chrome()
        
if __name__ == "__main__":
    # for i in range(30):
    #     output_file_path = f"basic_tests/test{i+1}.flow"  # Change this to your desired file path
    #     automate(output_file_path, i)
    automate("basic_tests/test.flow", 31)

