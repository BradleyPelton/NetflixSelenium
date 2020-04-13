import unittest

from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import secrets
import pagemodels.homepage
import pagemodels.showtoolspage
import tests.test_loginpage

# # - ROWS: Queue, genre , continue watching , trending now, similars, because you added,\
# # new release, top ten, netflix originals, popular titles, big row, most watched

# IMPORTANT VOCABULARY:
# Jawbone-
# Bob-container- AKA SHOW_PREVIEW
# show_element-
# row_element

# TEST CATEGORIES (CTRL + K + CTRL + 0 TO COLLAPSE ALL)
# 1.) ROW TESTS (e.g. row left row right)
# 2.) SHOW TESTS (e.g. upvote show, add show to my list)
# 2a- PLAY TESTS
# 2b-MY LIST TESTS
# 2c- UPVOTE/DOWNVOTE TESTS
# 2d- GENERAL DATA INTEGRITY(show_preview maturity rating agrees with jawbone maturity rating)

class HomePageTests(unittest.TestCase):
    """ tests for the homepage of netflix. AKA netflix.com/browse"""

    @classmethod
    def setUpClass(cls):
        """ launch the webdriver and login. See tests.pickledlogin for more"""
        chromedriver_path = secrets.chromedriver_path
        cls.driver = webdriver.Chrome(executable_path=chromedriver_path)
        tests.pickledlogin.pickled_login(cls.driver)

    @classmethod
    def tearDownClass(cls):
        """ TODO-"""
        cls.driver.quit()

    def setUp(self):
        """ load some random movie, Minority Report with Tom Cruise in this instance """
        self.driver.get("https://www.netflix.com/browse")

    # ROW FUNCTIONS/OPERATIONS
    def test_scroll_right_queue_row(self):
        """ """
        # TODO- UNTESTED
        home_page = pagemodels.homepage.HomePage(self.driver)
        queue_row = home_page.get_queue_row()
        home_page.row_page_right(queue_row)

        # I need to add an assert here
        # Maybe I need a function like displayed_shows(row_element) that prints the currently
        # displayed shows. Complication- Resolution

    def test_scroll_left_queue_row(self):
        """ """
        # TODO- UNTESTED
        # have to scroll right before scroll left is an option
        home_page = pagemodels.homepage.HomePage(self.driver)
        queue_row = home_page.get_queue_row()
        home_page.row_page_right(queue_row)
        home_page.row_page_left(queue_row)

    # def test_open_explore_all_first_genre_row(self):
    #     """ some rows have an "Explore all" button next to the title of the row"""
    #     """ TODO- ADD THIS FUCNTIONALITY TO homepage.py, then write this test"""
    #     pass

    # SHOW FUNCTIONS (see showtoolspage.py)
    # PLAY TESTS
    def test_play_first_show_in_my_list_from_jawbone(self):
        pass

    def test_play_first_show_in_my_list_from_show_preview(self):
        pass

    def test_play_first_show_in_continue_watching_row(self):
        pass

    def test_play_random_show(self):
        pass


    # ADD/REMOVE MY LIST TESTS
    def test_add_show_to_my_list_from_jawbone(self, show_element):
        """ add show to my list and assert that the show is now in my-list row"""
        # TODO- UNTESTED
        home_page = pagemodels.homepage.HomePage(self.driver)
        queue_row = home_page.get_queue_row()
        current_queue_list = home_page.get_row_titles_from_row_list(queue_row)

        show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)
        show_tools.add_show_to_my_list(show_element)

        # I WONDER IF I HAVE TO REFRESH?????? TODO TEST
        new_queue_list = home_page.get_row_titles_from_row_list(queue_row)

        self.assertEqual(current_queue_list + [show_element.title], new_queue_list)

    def test_remove_show_from_my_list_from_jawbone(self, show_element):
        """ remove a show from my-list from the jawbone
        and assert that the show is not in my-list row"""
        # TODO- UNTESTED
        home_page = pagemodels.homepage.HomePage(self.driver)
        queue_row = home_page.get_queue_row()
        current_queue_list = home_page.get_row_titles_from_row_list(queue_row)

        show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)
        show_tools.remove_show_from_my_list(show_element)

        # I WONDER IF I HAVE TO REFRESH?????? TODO TEST
        new_queue_list = home_page.get_row_titles_from_row_list(queue_row)

        self.assertEqual(current_queue_list.pop(show_element.title), new_queue_list)

    def test_add_show_to_my_list_from_show_preview(self, show_element):
        """ add show to my list from the show preview
        and assert that the show is now in my-list row"""
        # TODO- UNTESTED
        home_page = pagemodels.homepage.HomePage(self.driver)
        queue_row = home_page.get_queue_row()
        current_queue_list = home_page.get_row_titles_from_row_list(queue_row)

        show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)
        show_tools.add_show_to_my_list_from_show_preview(show_element)

        # I WONDER IF I HAVE TO REFRESH?????? TODO TEST
        new_queue_list = home_page.get_row_titles_from_row_list(queue_row)

        self.assertEqual(current_queue_list + [show_element.title], new_queue_list)

    def test_remove_show_from_my_list_from_show_preview(self, show_element):
        """ remove a show from my list from the show_preview
        and assert that the show is not in my-list(queue) row"""
        # TODO- UNTESTED
        home_page = pagemodels.homepage.HomePage(self.driver)
        queue_row = home_page.get_queue_row()
        current_queue_list = home_page.get_row_titles_from_row_list(queue_row)

        show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)
        show_tools.remove_show_from_my_list_from_show_preview(show_element)

        # I WONDER IF I HAVE TO REFRESH?????? TODO TEST
        new_queue_list = home_page.get_row_titles_from_row_list(queue_row)

        self.assertEqual(current_queue_list.pop(show_element.title), new_queue_list)

    # UPVOTE/DOWNVOTE TESTS
    def test_upvote_show_from_jawbone(self, show_element):
        """ upvote from the jawbone and assert upvoted"""
        pass

    def test_downvote_show_from_jawbone(self, show_element):
        pass

    def test_upvote_show_from_show_preview(self, show_element):
        pass

    def test_downvote_show_from_show_preview(self, show_element):
        pass

