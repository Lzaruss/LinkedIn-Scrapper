from src.ConfigManager import ConfigValidator, FileManager
from src.linkedIn_authenticator import LinkedInAuthenticator
from src.linkedIn_conector import LinkedInConector
from src.utils import chromeBrowserOptions, printred, printyellow

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException, TimeoutException

from pathlib import Path

def init_browser() -> webdriver.Chrome:
    try:
        options = chromeBrowserOptions()
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize browser: {str(e)}")

def main():
    browser = None
    try:
        data_folder = Path("data_folder")
        secrets_file, connections_links_file = FileManager.validate_data_folder(data_folder)
        email, password = ConfigValidator.validate_secrets(secrets_file)

        printyellow("Initializing browser...")
        browser = init_browser()

        printyellow("Starting LinkedIn authentication and data gathering...")
        auth = LinkedInAuthenticator(driver=browser)
        conector = LinkedInConector(connections_links_file, driver=browser)

        auth.set_secrets(email, password)
        auth.start()
        conector.start()

    except FileNotFoundError as e:
        printred(f"File error: {e}")
    except ValueError as e:
        printred(f"Configuration error: {e}")
    except WebDriverException as e:
        printred(f"Browser error: {e}")
    except TimeoutException as e:
        printred(f"Timeout error: {e}")
    except Exception as e:
        printred(f"Unexpected error: {e}")
    finally:
        if browser:
            printyellow("Closing browser...")
            browser.quit()

if __name__ == "__main__":
    main()
