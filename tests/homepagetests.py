import unittest

from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException

import pagemodels.homepage
import tests.logintests

# THE DRIVER IS HANDLED BY THE LOGINTESTS AND THEN PASSED FROM TEST OBJECT TO TEST OBJECT
# chromedriver_path = prerefactor.secrets.chromedriver_path
# driver = webdriver.Chrome(executable_path=chromedriver_path)

login_container = tests.logintests.LoginTests()
login_container.user_login_main()
# TODO- rename this. its not a login_container


class HomePageTests(unittest.TestCase):

    def __init__(self):
        self.driver = login_container.driver
        # this is a temporary patch for a larger problem, namely what to do with the driver
        # I need to be able to pass the driver from page object to page object 
        # Also these tests need to be able to work stand alone, and eventually, chained together

    def scroll_right_queue_row(self):
        home_page = pagemodels.homepage.HomePage(self.driver)
        queue_row = home_page.get_queue_row()
        home_page.row_page_right(queue_row)

    def scroll_left_queue_row(self):
        """have to scroll right before scroll left is an option"""
        home_page = pagemodels.homepage.HomePage(self.driver)
        queue_row = home_page.get_queue_row()
        home_page.row_page_right(queue_row)
        home_page.row_page_left(queue_row)


a = HomePageTests()
a.scroll_right_queue_row()
