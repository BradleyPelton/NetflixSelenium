import unittest
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import secrets
import pagemodels.loginpage

# Fully functional. All 4 tests passing.
# TODO- Clean it up and make it pretty
# TODO- Remove time.sleeps

class LoginPageTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ launch the webdriver """
        chromedriver_path = secrets.chromedriver_path
        cls.driver = webdriver.Chrome(executable_path=chromedriver_path)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        """navigate to the login page"""
        self.driver.get('https://www.netflix.com/login')

    def tearDown(self):
        """delete all cookies in case the login was successful"""
        self.driver.delete_all_cookies()

    def test_correct_user_login(self):
        login_page = pagemodels.loginpage.LoginPage(self.driver)
        login_page.user_login(
            secrets.bradleys_email, secrets.bradleys_password
        )
        # Recall there is an explicit wait built into login_page.user_login()
        time.sleep(2)
        self.assertTrue(login_page.login_successful())

    def test_user_login_incorrect_password(self):
        """ correct email but incorrect password """
        login_page = pagemodels.loginpage.LoginPage(self.driver)
        login_page.fake_login(
            secrets.bradleys_email, "FAKEPASSWORD123"
        )
        # Recall there is an explicit wait built into login_page.user_login()
        time.sleep(2)
        self.assertFalse(login_page.login_successful())

    def test_user_login_incorrect_email(self):
        """ incorrect email but registered password """
        login_page = pagemodels.loginpage.LoginPage(self.driver)
        login_page.fake_login(
            "fakeemail@email.com", secrets.bradleys_password
        )
        time.sleep(2)
        self.assertFalse(login_page.login_successful())

    def test_no_credentials_submit(self):
        """ submit the completely blank email and password fields"""
        login_page = pagemodels.loginpage.LoginPage(self.driver)
        login_page.fake_login(
            "", ""
        )
        time.sleep(2)
        self.assertFalse(login_page.login_successful())


# if __name__ == "__main__":
#     unittest.main()
