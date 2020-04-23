import unittest
import time

# from selenium import webdriver

import browserconfig
import pagemodels.homepage
import pagemodels.showtoolspage
import tests.test_loginpage
import tests.pickledlogin

# IMPORTANT VOCABULARY:
# Jawbone- Large menu displayed when clicking on show_element. Houses 99% of show information
# Bob-container/show-preview - mousing over a show displays upvote,downvote, play buttons
# show_element- uniform element that represents a show across this entire test suite
# row_element- uniform element that represents a row(containing show_elements)

# TEST CATEGORIES (CTRL + K + CTRL + 0 TO COLLAPSE ALL)
# 1.) ROW TESTS (e.g. row left row right)
# 2.) SHOW TESTS (e.g. upvote show, add show to my list)
# 2a- PLAY TESTS
# 2b- MY LIST TESTS
# 2c- UPVOTE/DOWNVOTE TESTS
# 2d- GENERAL DATA INTEGRITY TODO(show_preview maturity rating agrees with jawbone maturity rating)

# VIDEO OF EXECUTION
#  https://gyazo.com/8c9e75c1412c7e13e32b0b4bc14a5677

########################################################
########################################################
########################################################
## 2020-04-23 I cheated and introduced time.sleeps into jawbone open and mouse_over
# ALL TESTS PASSED 3 EXECUTIONS IN A ROW
# ALL OF THE PROBLEMS ORIGINATE FROM THE BOBCONTAINER AND JAWBONE LOADING
########################################################
########################################################
########################################################

# TODO- tests still don't perfectly clean up after themselves. Add more cleanup tasks
# namely, removing a show from my-list is complicated. Once removed, I would have to search for it


class HomePageTests(unittest.TestCase):
    """Tests for the homepage of netflix, AKA netflix.com/browse ."""

    @classmethod
    def setUpClass(cls):
        """Launch the webdriver of choice with selected options(see browserconfig.py).
        Then login using pickled cookies(see tests/pickledlogin.py)."""
        if browserconfig.current_browser in ['chrome', 'firefox']:
            cls.driver = browserconfig.driver_runner(
                executable_path=browserconfig.driver_path,
                desired_capabilities=browserconfig.capabilities
            )
        elif browserconfig.current_browser == 'edge':
            cls.driver = browserconfig.driver_runner(
                executable_path=browserconfig.driver_path,
                capabilities=browserconfig.capabilities
            )
        tests.pickledlogin.pickled_login(cls.driver)

    @classmethod
    def tearDownClass(cls):
        """Closes the browser and shuts down the driver executable."""
        cls.driver.quit()

    def setUp(self):
        """Navigate to the home page."""
        self.driver.get("https://www.netflix.com/browse")

    # # ROW FUNCTIONS/OPERATIONS
    def test_scroll_right_queue_row(self):
        """Scroll right in the queue/mylist row and assert the displayed shows have changed."""
        home_page = pagemodels.homepage.HomePage(self.driver)
        queue_row = home_page.get_queue_row()

        current_shows = home_page.get_currently_displayed_in_row(queue_row)
        current_shows_titles = [show.text for show in current_shows]

        home_page.row_page_right(queue_row)

        new_queue_row = home_page.get_queue_row()
        new_shows = home_page.get_currently_displayed_in_row(new_queue_row)
        new_show_titles = [show.text for show in new_shows]

        intersection_titles = [title for title in new_show_titles if title in current_shows_titles]

        # Assert that the list of displayed shows has changed entirely.
        self.assertTrue(intersection_titles == [])

    def test_scroll_left_queue_row(self):
        """Scroll right then left in the queue/mylist row and assert the displayed shows have
        changed."""
        # Have to scroll right before scroll left is an option.
        home_page = pagemodels.homepage.HomePage(self.driver)
        queue_row = home_page.get_queue_row()

        home_page.row_page_right(queue_row)
        home_page.row_page_right(queue_row)

        current_shows = home_page.get_currently_displayed_in_row(queue_row)
        current_shows_titles = [show.text for show in current_shows]

        home_page.row_page_left(queue_row)

        new_queue_row = home_page.get_queue_row()
        new_shows = home_page.get_currently_displayed_in_row(new_queue_row)
        new_show_titles = [show.text for show in new_shows]

        intersection_titles = [title for title in new_show_titles if title in current_shows_titles]

        # Assert that the list of displayed shows has changed entirely.
        self.assertTrue(intersection_titles == [])

    # SHOW FUNCTIONS (see showtoolspage.py)
    # PLAY TESTS
    def test_play_first_show_in_my_list_from_jawbone(self):
        """Grab the first show in my-list/queue and play it from the jawbone."""
        home_page = pagemodels.homepage.HomePage(self.driver)
        show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)

        queue_row = home_page.get_queue_row()

        first_show = home_page.get_first_show_in_row(queue_row)

        show_tools.play_show_from_jawbone(first_show)

        # 'watch' is always in the url for the netflix akira player.
        self.assertIn('watch', self.driver.current_url)

    def test_play_first_show_in_my_list_from_show_preview(self):
        """Grab the first show in my-list/queue and play it from the show_preview/bob-container."""
        home_page = pagemodels.homepage.HomePage(self.driver)
        queue_row = home_page.get_queue_row()

        first_show = home_page.get_first_show_in_row(queue_row)

        show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)
        show_tools.play_show_from_show_preview(first_show)

        # 'watch' is always in the url for the netflix akira player.
        self.assertIn('watch', self.driver.current_url)

    def test_play_first_show_in_continue_watching_row(self):
        """Grab the first show in the 'continue watching row' and play it from the jawbone."""
        home_page = pagemodels.homepage.HomePage(self.driver)
        cont_watching_row = home_page.get_continue_watching_row()

        first_show = home_page.get_first_show_in_row(cont_watching_row)

        show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)
        show_tools.play_show_from_jawbone(first_show)

        # 'watch' is always in the url for the netflix akira player.
        self.assertIn('watch', self.driver.current_url)
        # TODO- This asserts that any show is being watched, not that first_show is being watched.
        # See if there is a way to assert the title is present somewhere.

    # # ADD/REMOVE MY LIST TESTS
    def test_add_show_to_my_list_from_jawbone(self):
        """Add show to my list and assert that the show is now in my-list row."""
        home_page = pagemodels.homepage.HomePage(self.driver)
        show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)

        # We need to find a random show that is not in my list already.

        test_condition = show_tools.is_in_my_list_from_show_preview
        random_show = home_page.get_semi_random_show(
            condition=test_condition,
            condition_bool='False'
        )
        # get a random show that meets the condition and condition_bool, namely a show that
        # returns false when is_in_my_list(show), i.e. a show not in my list
        saved_title_name = random_show.text

        show_tools.close_show_preview()
        show_tools.add_show_to_my_list_from_jawbone(random_show)

        self.driver.get('https://netflix.com')

        new_queue_row = home_page.get_queue_row()
        new_shows = home_page.get_currently_displayed_in_row(new_queue_row)
        new_show_titles = [show.text for show in new_shows]

        self.assertIn(saved_title_name, new_show_titles)

    def test_remove_show_from_my_list_from_jawbone(self):
        """Remove the first show from my-list/queue from the jawbone and assert that the show is
        not in my-list/queue row after."""
        home_page = pagemodels.homepage.HomePage(self.driver)
        queue_row = home_page.get_queue_row()

        first_show_in_q = home_page.get_first_show_in_row(queue_row)
        first_show_in_q_title = first_show_in_q.text

        show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)
        show_tools.remove_show_from_my_list_from_jawbone(first_show_in_q)

        self.driver.get('https://netflix.com')

        new_queue_row = home_page.get_queue_row()
        new_shows = home_page.get_currently_displayed_in_row(new_queue_row)
        new_show_titles = [show.text for show in new_shows]

        self.assertNotIn(first_show_in_q_title, new_show_titles)

    def test_add_show_to_my_list_from_show_preview(self):
        """Add a random show to my list with the show preview and assert that the show is now in
        my-list/queue row."""
        home_page = pagemodels.homepage.HomePage(self.driver)
        show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)

        # We need to find a random show that is not in my list already.

        test_condition = show_tools.is_in_my_list_from_show_preview
        random_show = home_page.get_semi_random_show(
            condition=test_condition,
            condition_bool='False'
        )
        # get a random show that meets the condition and condition_bool, namely a show that
        # returns false when is_in_my_list(show), i.e. a show not in my list
        saved_title_name = random_show.text

        show_tools.add_show_to_my_list_from_show_preview(random_show)

        self.driver.get('https://netflix.com')

        new_queue_row = home_page.get_queue_row()
        new_shows = home_page.get_currently_displayed_in_row(new_queue_row)
        new_show_titles = [show.text for show in new_shows]

        self.assertIn(saved_title_name, new_show_titles)

    def test_remove_show_from_my_list_from_show_preview(self):
        """Remove a show from my-list/queue via the show_preview and assert that the show is not in
        my-list/queue row."""
        home_page = pagemodels.homepage.HomePage(self.driver)
        show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)

        queue_row = home_page.get_queue_row()
        first_queue_show = home_page.get_first_show_in_row(queue_row)
        saved_title_name = first_queue_show.text

        # show_tools.mouse_over_show_element(first_queue_show)
        show_tools.third_remove_from_my_list_from_show_preview(first_queue_show)

        # Relaunching the page to see if the show has been removed from my_list
        self.driver.get("https://netflix.com/browse")

        new_queue_row = home_page.get_queue_row()
        new_shows = home_page.get_currently_displayed_in_row(new_queue_row)
        new_show_titles = [show.text for show in new_shows]

        self.assertNotIn(saved_title_name, new_show_titles)

    # # # # # UPVOTE/DOWNVOTE TESTS
    def test_upvote_show_from_jawbone(self):
        """Upvote a random show from the jawbone and assert upvoted."""
        home_page = pagemodels.homepage.HomePage(self.driver)
        show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)

        test_condition = show_tools.is_upvoted_from_show_preview
        random_show = home_page.get_semi_random_show(
            condition=test_condition,
            condition_bool='false'
        )
        # Find a random show that is not already upvoted

        show_tools.close_show_preview()
        show_tools.upvote_from_jawbone(random_show)
        self.assertTrue(show_tools.is_upvoted_from_jawbone(random_show))

        # CLEANUP
        show_tools.remove_downvote_or_upvote_from_jawbone(random_show)

    def test_downvote_show_from_jawbone(self):
        """Downvote a random show from the jawbone and assert downvoted."""
        home_page = pagemodels.homepage.HomePage(self.driver)
        show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)

        test_condition = show_tools.is_downvoted_from_show_preview
        random_show = home_page.get_semi_random_show(
            condition=test_condition,
            condition_bool='false'
        )
        # Find a random show that is not already downvoted

        show_tools.close_show_preview()
        show_tools.open_jawbone_if_not_open(random_show)
        show_tools.downvote_from_jawbone(random_show)

        self.assertTrue(show_tools.is_downvoted_from_jawbone(random_show))

        # CLEANUP
        show_tools.remove_downvote_or_upvote_from_jawbone(random_show)

    def test_upvote_show_from_show_preview(self):
        """Upvote a random show from the show preview and assert its upvoted."""
        home_page = pagemodels.homepage.HomePage(self.driver)
        show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)

        test_condition = show_tools.is_upvoted_from_show_preview
        random_show = home_page.get_semi_random_show(
            condition=test_condition,
            condition_bool='false'
        )
        # Find a random show that is not already upvoted

        show_tools.upvote_from_show_preview(random_show)

        self.assertTrue(show_tools.is_upvoted_from_show_preview(random_show))

        # CLEANUP
        show_tools.remove_downvote_or_upvote_from_show_preview(random_show)

    def test_downvote_show_from_show_preview(self):
        """Downvote a random show from the show preview and assert its downvoted."""
        home_page = pagemodels.homepage.HomePage(self.driver)
        show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)

        # home_page.scroll_to_bottom_of_page()

        test_condition = show_tools.is_downvoted_from_show_preview
        random_show = home_page.get_semi_random_show(
            condition=test_condition,
            condition_bool='false'
        )
        # Find a random show that is not already downvoted

        show_tools.downvote_from_show_preview(random_show)

        self.assertTrue(show_tools.is_downvoted_from_show_preview(random_show))

        # CLEANUP
        show_tools.remove_downvote_or_upvote_from_show_preview(random_show)

    # # # TESTS THAT DIDNT MAKE THE FIRST CUT
    # # # # def test_open_explore_all_first_genre_row(self):
    # # # #     """ some rows have an "Explore all" button next to the title of the row"""
    # # # #     """ TODO- ADD THIS FUCNTIONALITY TO homepage.py, then write this test"""
    # # # #     pass

    # # # # def test_play_random_show(self):
    # # # #     """ not really a test but a cool function I want to have somewhere"""
    # # # #     pass
