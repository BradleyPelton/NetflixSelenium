from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from pagemodels.basepage import BasePage

# TODO STILL NEEDS WORK
# TEST ISNT FINDING ERROR MESSAGE FOR INCORRECT LOGIN

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # LOCATORS
        self.USERNAME_FIELD = (By.CSS_SELECTOR, 'input[name="userLoginId"]')
        self.PASSWORD_FIELD = (By.CSS_SELECTOR, 'input[name="password"]')
        self.ERROR_MESSAGE = (By.CSS_SELECTOR, 'div.error-message-container')
        self.HOME_BUTTON = (By.CSS_SELECTOR, 'a.logo.icon-logoUpdate.active')
        self.INVALID_USERNAME_MESSAGE = (By.CSS_SELECTOR, 'div[data-uia="login-field+error"]')
        self.INVALID_PASSWORD_MESSAGE = (By.CSS_SELECTOR, 'div[data-uia="password-field+error"]')

    def user_login(self, username, password):
        """NOT MEANT FOR TESTING. meant to be used by setUpClasses and pickledLogin"""
        username_field = self.driver.find_element(*self.USERNAME_FIELD)
        username_field.send_keys(username)

        password_field = self.driver.find_element(*self.PASSWORD_FIELD)
        password_field.send_keys(password)
        password_field.submit()

        # Wait for the login to finish
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located(self.HOME_BUTTON))

    def fake_login(self, username, password):
        """ login that is expected to fail. Works exactly the same as user_login and will even
        successfully login if passed correct credentials. Splitting the two for sanity's sake"""
        username_field = self.driver.find_element(*self.USERNAME_FIELD)
        username_field.send_keys(username)

        password_field = self.driver.find_element(*self.PASSWORD_FIELD)
        password_field.send_keys(password)
        password_field.submit()

    def login_successful(self):
        """ return true if login failed, false if else"""
        try:
            self.driver.find_element(*self.ERROR_MESSAGE)  # Error message if invalid combination
            return False
        except NoSuchElementException:
            # print("didnt find the error message for invalid combination")
            pass
        try:
            self.driver.find_element(*self.HOME_BUTTON)
            return True
        except NoSuchElementException:
            print("login_successful COULDNT DTERMINE EITHER LOGGED IN OR NOT, SOMETHING BROKE")

    def is_invalid_password(self):
        """ return true if a the warning is present for an invalid password"""
        # Invalid implies password is not between 4 and 60 characters. Could be missing entirely
        try:
            self.driver.find_element(*self.INVALID_PASSWORD_MESSAGE)
            return True
        except NoSuchElementException:
            return False

    def is_invalid_username(self):
        """ return true if the warning is present for an invalid username """
        # Invalid username implies invalid email or phone number. Could be missing entirely
        try:
            self.driver.find_element(*self.INVALID_USERNAME_MESSAGE)
            return True
        except NoSuchElementException:
            return False
