import unittest

from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException

import prerefactor.secrets
import pagemodels.loginpage

# SET YOUR PATH TO YOUR CHROMEDRIVER
chromedriver_path = prerefactor.secrets.chromedriver_path
driver = webdriver.Chrome(executable_path=chromedriver_path)


class LoginTests(unittest.TestCase):

    def user_login_main(self):
        login_page = pagemodels.loginpage.LoginPage(driver)
        login_page.load()
        login_page.user_login(
            prerefactor.secrets.bradleys_email, prerefactor.secrets.bradleys_password
        )
        # print("login was successfull?")

    # def user_login_incorrect_password(self):
    #     """ """
    #     pass

a = LoginTests()
a.user_login_main()