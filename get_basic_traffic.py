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

def accept_buttons(page):
    """Handle button clicking logic using Playwright."""
    try:
        if page.locator('xpath=//*[@id="declineButton"]').is_visible():
            page.click('xpath=//*[@id="declineButton"]')
            print("Clicked 'declineButton'")
    except Exception as e:
        print(f"Error clicking 'declineButton': {e}")

    try:
        if page.locator('xpath=//*[@id="ackButton"]').is_visible():
            page.click('xpath=//*[@id="ackButton"]')
            print("Clicked 'ackButton'")
    except Exception as e:
        print(f"Error clicking 'ackButton': {e}")

def automate(output_file, i):
        start_chrome(i+4)
        process = mitm(output_file)
        time.sleep(10)
        # with sync_playwright() as p:
        #     browser = p.chromium.launch(headless=False)  # Set headless=True for background mode
        #     page = browser.new_page()
        #     page.goto("about:blank")  # No specific URL, just open a blank page
        #     accept_buttons(page)
        #     browser.close()
        # close_mitm(process)
        close_chrome()
        
if __name__ == "__main__":
    # Specify the output file path for mitmweb flows
    for i in range(30):
        output_file_path = f"basic_tests/test{i+1}.flow"  # Change this to your desired file path
        automate(output_file_path, i)
