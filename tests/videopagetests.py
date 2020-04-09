import unittest

from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException

import pagemodels.videopage
import tests.logintests

login_container = tests.logintests.LoginTests()
login_container.user_login_main()
# TODO- rename this. its not a login_container


class VideoPageTests(unittest.TestCase):

    def __init__(self):
        self.driver = login_container.driver

    def wake_up(self):
        """wake up"""
        video_page = pagemodels.videopage.VideoPage(self.driver)
        video_page.wake_up_idle_player()


b = pagemodels.videopage.VideoPage(login_container.driver)
a = VideoPageTests()
a.wake_up()
