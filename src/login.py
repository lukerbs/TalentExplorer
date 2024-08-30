import time
from selenium.webdriver.common.by import By

def login(driver, username, password):
    # - - LOG IN PAGE - -
    # Find the element by the autocomplete attribute
    username_field = driver.find_element(By.CSS_SELECTOR, 'input[autocomplete="username"]')
    username_field.send_keys(username)
    time.sleep(3)

    password_field = driver.find_element(By.ID, 'session_password')
    password_field.send_keys(password)
    time.sleep(1)

    sign_in_btn = driver.find_element(By.CSS_SELECTOR, 'button[data-id="sign-in-form__submit-btn"]')
    sign_in_btn.click()
    time.sleep(6)

    # wait for challenge if necessary
    page_text = driver.find_element(By.XPATH, "/html/body").text.lower()
    if 'challenge' in page_text or 'verification' in page_text or 'security' in page_text:
        input('Submit verification code and press enter:')
    time.sleep(3)