import unittest

# from selenium import webdriver

import pagemodels.headerpage
import tests.pickledlogin
import browserconfig

# VIDEO OF EXECUTION
# https://gyazo.com/b20fd223076bf34c1f2c9b94a4f1fe0a

# 2020-04-20 All tests passing, refactor complete


class HeaderPageTests(unittest.TestCase):
    """ test cases for the use of the header features atop most netflix pages"""
    @classmethod
    def setUpClass(cls):
        """ launch the webdriver of choice with selected options. (SEE browserconfig.py)
         and then login using pickled cookies. (SEE tests/pickledlogin.py)"""
        if browserconfig.current_browser in ['chrome', 'firefox']:
            cls.driver = browserconfig.driver_runner(
                executable_path=browserconfig.driver_path,
                desired_capabilities=browserconfig.capabilities
            )
        elif browserconfig.current_browser == 'edge':
            cls.driver = browserconfig.driver_runner(
                executable_path=browserconfig.driver_path,
                desired_capabilities=browserconfig.capabilities
            )
        tests.pickledlogin.pickled_login(cls.driver)

    @classmethod
    def tearDownClass(cls):
        """ closes the browser and shuts down the driver executable"""
        cls.driver.quit()

    def setUp(self):
        """ return to the home page, netflix.com/browse, the staging place for header tests"""
        self.driver.get("https://netflix.com/browse")

    def test_logout_from_header(self):
        """ logout from the header """
        header_page = pagemodels.headerpage.HeaderPage(self.driver)

        header_page.logout()
        # user is redirected to https://www.netflix.com/logout after loging out

        self.assertIn('logout', self.driver.current_url)

        # CLEANUP
        # log back in using the pickled cookies
        tests.pickledlogin.pickled_login(self.driver)

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
        # I kind of like this assert now that I think about it. Its testing both the search
        # function and Netflix's search algorithm.
        # NOTE- test will not fail if "The Shawkshank Redemeption" is removed. Netflix displays
        # "similar to {title_name}" for titles its search algorithm recognizes

    def test_click_top_notification(self):
        """ click the top notification and assert that the page has changed"""
        header_page = pagemodels.headerpage.HeaderPage(self.driver)

        header_page.click_top_notification()

        # assert that we navigated to a notification page or a title page(only 2 options)
        self.assertTrue(
            'title' in self.driver.current_url or 'notification' in self.driver.current_url
        )

    # DIDNT MAKE THE FIRST CUT OF TESTS
    # I could have 5 more test here for each one of the header buttons.
    # Those are about as elementary of tests as possible. Skipping them but TODO- OKAY TO HAVE

        # def test_clear_all_notifications(self):
    #     """ this is easy to do, but impossible to perfect. Netflix doesnt allow any sort of
    #     'mark notification as unread' so I have no way of generating notifications. Since I have
    #     no way of managing the state, THIS TEST CAN NEVER BE RAN MORE THAN ONCE A DAY. Thus I am
    #     forced to leave it out in order to avoid inconsistent test results"""
    #     header_page = pagemodels.headerpage.HeaderPage(self.driver)

    #     header_page.clear_notifications()
