import unittest

from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import pagemodels.homepage
import tests.test_loginpage

# THE DRIVER IS HANDLED BY THE LOGINTESTS AND THEN PASSED FROM TEST OBJECT TO TEST OBJECT
# chromedriver_path = prerefactor.secrets.chromedriver_path
# driver = webdriver.Chrome(executable_path=chromedriver_path)

login_container = tests.test_loginpage.LoginTests()
login_container.user_login_main()
# TODO- rename this. its not a login_container

# TODO- a solution to this, and a recommendation from the docs is not to automate login.
# Eliminating logging in via webbrowser before every test will improve both the speed and stability
# of the test. A method should be created to gain access to the AUT* (e.g. using an API to login
# and set a cookie).


class HomePageTests(unittest.TestCase):

    def setUp(self):
        self.driver = login_container.driver
        # this is a temporary patch for a larger problem, namely what to do with the driver
        # I need to be able to pass the driver from page object to page object 
        # Also these tests need to be able to work stand alone, and eventually, chained together

    def test_scroll_right_queue_row(self):
        home_page = pagemodels.homepage.HomePage(self.driver)
        queue_row = home_page.get_queue_row()
        home_page.row_page_right(queue_row)

    def test_scroll_left_queue_row(self):
        """have to scroll right before scroll left is an option"""
        home_page = pagemodels.homepage.HomePage(self.driver)
        queue_row = home_page.get_queue_row()
        home_page.row_page_right(queue_row)
        home_page.row_page_left(queue_row)

    def tearDown(self):
        pass



a = HomePageTests()
a.scroll_right_queue_row()
