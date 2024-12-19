import os
import subprocess
from playwright.sync_api import sync_playwright
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def accept_form(driver):
    time.sleep(5)
    try:
        decline_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="declineButton"]'))
        )
        decline_button.click()
        print("Clicked 'declineButton'")
    except Exception as e:
        print(f"Error clicking 'declineButton': {e}")

    try:
        ack_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="ackButton"]'))
        )
        ack_button.click()
        print("Clicked 'ackButton'")
    except Exception as e:
        print(f"Error clicking 'ackButton': {e}")

def add_extension():
    pass

def question_prompts():
    pass

def close():
    pass

def ask():
    chrome_options = Options()
    chrome_options.add_argument('--user-data-dir=/Users/alexanderciechonski/Library/Application Support/Google/Chrome/Profile 5')
    chrome_options.add_argument('--profile-directory=Profile 5')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_extension("/Users/alexanderciechonski/Library/Application Support/Google/Chrome/Default/Extensions/hlgbcneanomplepojfcnclggenpcoldo/1.0.21_0.crx")
    driver = webdriver.Chrome(options=chrome_options)
    time.sleep(1)
    driver.get("chrome-extension://hlgbcneanomplepojfcnclggenpcoldo/index.html")
    time.sleep(20)

def open_browser(i):
    try:
        kill = [
            "pkill", "-9", "chrome"
        ]
        subprocess.run(kill, check=True)
    except subprocess.CalledProcessError:
        print("No Chrome processes were running.")

    command = [
        "open", "-na", "Google Chrome", "--args", 
        '--no-first-run',
        '--no-default-browser-check',
        f"--profile-directory=Profile {i}",
        "--remote-debugging-port=9222"
    ]
    subprocess.run(command, check=True)

def connect_browser(extension_path):
    print('browser launched')
    time.sleep(10)
    chrome_options = Options()
    chrome_options.add_extension(extension_path)
    chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
    driver = webdriver.Chrome(options=chrome_options)

    print('connected')
    driver.get("https://www.ucl.ac.uk/isd/services/learning-teaching/moodle")
    time.sleep(2)
    driver.quit()
    return driver


def main():
    extension_path = "/Users/alexanderciechonski/Library/Application Support/Google/Chrome/Default/Extensions/hlgbcneanomplepojfcnclggenpcoldo/1.0.21_0.crx"
    open_browser(50)
    driver = connect_browser(extension_path)
    # accept_form(driver)


if __name__ == "__main__":
    ask()