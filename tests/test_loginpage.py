import unittest

from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException

import secrets
import pagemodels.loginpage

# THIS WILL BE THE ONLY PLACE WHERE driver IS DEFINED. EVERY OTHER TEST OBJECT WILL BE PASSED
# THE driver FROM THIS TEST OBJECT
# SET YOUR PATH TO YOUR CHROMEDRIVER

chromedriver_path = secrets.chromedriver_path
driver = webdriver.Chrome(executable_path=chromedriver_path)



class LoginTests(unittest.TestCase):

    def __init__(self):
        self.driver = driver

    def setUp(self):
        """ """
        pass

    def test_user_login_main(self):
        login_page = pagemodels.loginpage.LoginPage(driver)
        login_page.load()
        login_page.user_login(
            secrets.bradleys_email, secrets.bradleys_password
        )
        # Recall there is an explicit wait built into login_page.user_login()
        self.assertEqual('https://www.netflix.com/browse', driver.current_url)

    def test_user_login_incorrect_credentials(self):
        """ """
        pass

    def test_user_login_incorrect_email(self):
        """ """
        pass

    def tearDown(self):
        """ """
        pass
        # self.driver.quit()



if __name__ == "__main__":
    unittest.main()

