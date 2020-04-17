import unittest
import time

from selenium import webdriver

import pagemodels.headerpage
import tests.pickledlogin
import browserconfig

# VIDEO OF EXECUTION
# https://gyazo.com/b20fd223076bf34c1f2c9b94a4f1fe0a

class HeaderPageTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ launch the webdriver and login. See tests.pickled.login for more"""
        cls.driver = browserconfig.driver_runner(
            executable_path=browserconfig.driver_path,
            options=browserconfig.current_options
        )
        tests.pickledlogin.pickled_login(cls.driver)

    @classmethod
    def tearDownClass(cls):
        """ TODO-"""
        cls.driver.quit()

    def setUp(self):
        """ return to the home page, netflix.com/browse, the staging place for header tests"""
        self.driver.get("https://netflix.com/browse")

    # # (TEST CATEGORY NAME HERE?)
    def test_logout_from_header(self):
        """ logout from the header """
        header_page = pagemodels.headerpage.HeaderPage(self.driver)

        header_page.logout()
        # user is redirected to https://www.netflix.com/logout

        self.assertIn('logout', self.driver.current_url)

        # CLEANUP
        # log back in using the pickled cookies
        tests.pickledlogin.pickled_login(self.driver)
        time.sleep(5)

    def test_navigate_home_from_my_list(self):
        """ using the giant Netflix logo in the top left, navigate to the home page /browse/
        from my-list"""
        self.driver.get("https://www.netflix.com/browse/my-list")
        header_page = pagemodels.headerpage.HeaderPage(self.driver)

        header_page.navigate_to_home()

        self.assertEqual("https://www.netflix.com/browse", self.driver.current_url)

    def test_navigate_to_manage_profile(self):
        """ using the header account dropdown, navigate to the manage profile page"""
        header_page = pagemodels.headerpage.HeaderPage(self.driver)

        header_page.navigate_to_manage_profile()
        # user is redirected to https://www.netflix.com/profiles/manage

        self.assertIn('profiles/manage', self.driver.current_url)

    def test_search_for_shawshank(self):
        """using the search field, search for shawshank"""
        header_page = pagemodels.headerpage.HeaderPage(self.driver)

        header_page.search("shawshank")

        self.assertIn("The Shawshank Redemption", self.driver.page_source)
        # sloppy assert. I could build a function that finds the first show in the search box
        # TODO- NICE TO HAVE
        # I kind of like this assert now that I think about it. Its testing both the search
        # function and Netflix's search algorithm.

    # def test_clear_all_notifications(self):
    #     """ this is easy to do, but impossible to perfect. Netflix doesnt allow any sort of
    #     'mark notification as unread' so I have no way of generating notifications. Since I have
    #     no way of managing the state, THIS TEST CAN NEVER BE RAN MORE THAN ONCE A DAY. Thus I am
    #     forced to leave it out in order to avoid inconsistent test results"""
    #     header_page = pagemodels.headerpage.HeaderPage(self.driver)

    #     header_page.clear_notifications()

    def test_click_top_notification(self):
        """ click the top notification and assert that the page has changed"""
        header_page = pagemodels.headerpage.HeaderPage(self.driver)

        header_page.click_top_notification()

        time.sleep(3)

        # assert that we navigated to a different page
        # Possible options: title page or notification page
        self.assertTrue(
            'title' in self.driver.current_url or 'notification' in self.driver.current_url
        )

        # I could have 5 more test here for each one of the header buttons.
        # Those are about as elementary tests as possible. Skipping them but TODO- OKAY TO HAVE