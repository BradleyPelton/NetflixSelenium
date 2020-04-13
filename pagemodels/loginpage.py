from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from pagemodels.basepage import BasePage


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # RECALL BASE CLASS IS HANDLING self.driver = driver TODO- DELETE ME
        # LOCATORS
        # lo STANDS FOR LOCATOR
        self.USERNAME_FIELD = (By.CSS_SELECTOR, 'input[name="userLoginId"]')
        self.PASSWORD_FIELD = (By.CSS_SELECTOR, 'input[name="password"]')
        self.HOME_BUTTON = (By.CSS_SELECTOR, 'a.logo.icon-logoUpdate.active')
        # realistically the home button doesnt technically belong to this page... TODO

    def load(self):
        """ TODO- NOTE- this is purely a stylistic choice. Some people choose to force the load in
        the __init__ . I'm choosing to explicitly call load just to be overly cautious
        """
        self.driver.get('https://netflix.com/login')

    def user_login(self, username, password):
        """NOT MEANT FOR TESTING, MEANT TO BE USED BY OTHER TESTS"""

        username_field = self.driver.find_element(*self.USERNAME_FIELD)
        username_field.send_keys(username)

        password_field = self.driver.find_element(*self.PASSWORD_FIELD)
        password_field.send_keys(password)
        password_field.submit()

        # Explicit wait for the login to finish
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

        # REMOVED THE EXPLICIT WAIT HERE

    def login_successful(self):
        """ return true if login failed, false if else"""
        try:
            self.driver.find_element(*self.HOME_BUTTON)
            return True
        except NoSuchElementException:
            return False
        # TODO-Could be cleaner by testing that the error popup popped up
 