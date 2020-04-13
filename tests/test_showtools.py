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

# SHOWTOOLS IS NOT A PAGE, IT IS A COMMON SET OF TOOLS FOR THE HANDLING OF show_elements
# (see showtoolspage.py for more). show_elements are the universal element of the Netflix app
# and EVERY page consists of rows of show_elements.


# PRIMARY USE- the show tools are meant to be used in tests for homepage, mylist, genrepage, etc.
# TODO- Delete all of this? There are no tests specific to just show tools that arent covered
# elsewhere?
class ShowToolsTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ launch the webdriver and login. See tests.pickled.login for more"""
        chromedriver_path = secrets.chromedriver_path
        cls.driver = webdriver.Chrome(executable_path=chromedriver_path)
        tests.pickledlogin.pickled_login(cls.driver)

    @classmethod
    def tearDownClass(cls):
        """ TODO-"""
        cls.driver.quit()

    def setUp(self):
        """ load some random movie, Minority Report with Tom Cruise in this instance """
        pass  # TODO ?

    def play_show_from_jawbone(self, show_element):
        """wake up"""
        show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)
        show_tools.play_show(show_element)
        # UNTESTED TODO
