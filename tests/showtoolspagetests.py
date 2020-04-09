import unittest

from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException

import pagemodels.showtoolspage
import tests.logintests

login_container = tests.logintests.LoginTests()
login_container.user_login_main()
# TODO- rename this. its not a login_container


class VideoPageTests(unittest.TestCase):

    def __init__(self):
        self.driver = login_container.driver

    def play_show_from_jawbone(self, show_element):
        """wake up"""
        show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)
        show_tools.play_show(show_element)
        # UNTESTED TODO


a = VideoPageTests()
a.play_show_from_jawbone("sgjhdgs")