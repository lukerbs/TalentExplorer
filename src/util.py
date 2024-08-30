from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

def wait():
    """Pauses crawling process for manual intervention.
    """
    input('Press enter to continue: ')

def build_driver():
    """Creates a Selenium chrome driver with custom settings.

    Returns:
        webriver: A selenium webdriver with custom settings.
    """
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-agent={user_agent}")

    # Instantiate chrome web driver
    chrome_path = ChromeDriverManager().install()
    chrome_service = Service(chrome_path)
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return driver