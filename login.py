from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
# from selenium.common.exceptions import NoSuchElementException
import secrets

# SET YOUR PATH TO YOUR CHROMEDRIVER
chromedriver_path = secrets.chromedriver_path
# THIS WILL LAUNCH THE DRIVER EVERY TIME LOGIN IS IMPORTE
# SINCE EVERYTHING IS LOCKED BEHIND A USER BEING-LOGGED IN,
# LOGIN IS A NECESSARY AND REQUISITE STEP FOR EVERY TEST
driver = webdriver.Chrome(executable_path=chromedriver_path)



def user_login(username,password):
    """username, password case sensitive strings"""
    # Should the driver be passed to the function ? Consider after rewrite
    driver.get('https://netflix.com/login')


    username_field = driver.find_element_by_css_selector('input[name="userLoginId"]')
    username_field.send_keys(username)

    password_field = driver.find_element_by_css_selector('input[name="password"]')
    password_field.send_keys(password)
    password_field.submit()

if __name__ == "__main__":
    user_login(secrets.bradleys_email, secrets.bradleys_password)
