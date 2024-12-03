import os
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

chromeProfilePath = os.path.join(os.getcwd(), "chrome_profile", "linkedin_profile")

def ensure_chrome_profile():
    profile_dir = os.path.dirname(chromeProfilePath)
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)
    if not os.path.exists(chromeProfilePath):
        os.makedirs(chromeProfilePath)
    return chromeProfilePath

def scroll_to_end(driver, times=20):
        for _ in range(times):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                driver.find_element(By.CSS_SELECTOR, "div.p5").click() 
            except:
                pass

def chromeBrowserOptions():
    ensure_chrome_profile()
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  
    options.add_argument("--no-sandbox")  
    options.add_argument("--disable-dev-shm-usage") 
    options.add_argument("--ignore-certificate-errors")  
    options.add_argument("--disable-extensions")  
    options.add_argument("--disable-gpu") 
    options.add_argument("window-size=1200x800")  
    options.add_argument("--disable-background-timer-throttling") 
    options.add_argument("--disable-backgrounding-occluded-windows")  
    options.add_argument("--disable-translate")  
    options.add_argument("--disable-popup-blocking")  
    options.add_argument("--no-first-run")  
    options.add_argument("--no-default-browser-check")  
    options.add_argument("--disable-logging") 
    options.add_argument("--disable-autofill")
    options.add_argument("--disable-plugins") 
    options.add_argument("--disable-animations") 
    options.add_argument("--disable-cache") 
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"]) 

    prefs = {
        "profile.default_content_setting_values.images": 2,  
        "profile.managed_default_content_settings.stylesheets": 2,
    }
    options.add_experimental_option("prefs", prefs)

    if len(chromeProfilePath) > 0:
        initialPath = os.path.dirname(chromeProfilePath)
        profileDir = os.path.basename(chromeProfilePath)
        options.add_argument('--user-data-dir=' + initialPath)
        options.add_argument("--profile-directory=" + profileDir)
    else:
        options.add_argument("--incognito")

    return options


def printred(text):
    RED = "\033[91m"
    RESET = "\033[0m"
    print(f"{RED}{text}{RESET}")

def printyellow(text):
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    print(f"{YELLOW}{text}{RESET}")