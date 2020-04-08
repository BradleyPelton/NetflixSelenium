from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pagemodels.basepage import BasePage


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # RECALL BASE CLASS IS HANDLING self.driver = driver TODO- DELETE ME
        # LOCATORS
        # lo STANDS FOR LOCATOR
        self.LO_USERNAME_FIELD = (By.CSS_SELECTOR, 'input[name="userLoginId"]')
        self.LO_PASSWORD_FIELD = (By.CSS_SELECTOR, 'input[name="password"]')
        self.LO_HOME_BUTTON = (By.CSS_SELECTOR, 'a.logo.icon-logoUpdate.active')
        # realistically the home button doesnt technically belong to this page... TODO

    def load(self):
        """ TODO- NOTE- this is purely a stylistic choice. Some people choose to force the load in
        the __init__ . I'm choosing to explicitly call load just to be overly cautious
        """
        self.driver.get('https://netflix.com/login')

    def user_login(self, username, password):
        """username, password case sensitive strings"""

        username_field = self.driver.find_element(*self.LO_USERNAME_FIELD)
        username_field.send_keys(username)

        password_field = self.driver.find_element(*self.LO_PASSWORD_FIELD)
        password_field.send_keys(password)
        password_field.submit()

        # Explicit wait for the login to finish
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located(self.LO_HOME_BUTTON))
