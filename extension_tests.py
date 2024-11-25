import os
import subprocess
from playwright.sync_api import sync_playwright
import time

def open_browser(i):
    command = [
            "open", "-na", "Google Chrome", "--args", "--profile-directory=" + f"Profile {i}"
        ]
    subprocess.run(command, check=True)

def accept_form():
    pass

def add_extension():
    pass

def question_prompts():
    pass

def close():
    pass

def ask(i, questions):
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=f"/Users/alexanderciechonski/Library/Application Support/Google/Chrome/Profile {i+3}",  
            headless=False 
        )
        
        if browser.pages:
            page = browser.pages[0]  # Use the first page if it exists
        else:
            page = browser.new_page()  # Create a new page if no pages exist

        # Navigate and interact with the page
        page.goto("https://www.google.com")
        print("Navigated to Google")
        # browser = p.chromium.launch(headless=False)  
        # page = browser.new_page()
        # add_extension()
        # question_prompts()
        time.sleep(5)
        browser.close()


def main():
    with open('questions.txt', 'r') as f:
        questions = [line.strip() for line in f]

    # for i in range(30):
    #     ask(i, questions)
    ask(1, questions)