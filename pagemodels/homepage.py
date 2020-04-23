import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

import pagemodels.showtoolspage
from pagemodels.basepage import BasePage
import browserconfig
import secrets
import pagemodels.showtoolspage
import tests.pickledlogin

# # - ROWS: Queue, genre , continue watching , trending now, similars, because you added,\
# # new release, top ten, netflix originals, popular titles, big row, most watched


# The Home page for netflix is netflix.com/browse. Everything leads back to /browse

# RECALL A show_element HAS A VERY SPECIFIC FORMAT. THE NODE HAS TO BE AN A TAG LOCATED INSIDER
# 'div.slider-item > div > div > a.slider-refocus'



# DELETE ME
# driver = browserconfig.driver_runner(
#     executable_path=browserconfig.driver_path,
#     desired_capabilities=browserconfig.capabilities
# )
# tests.pickledlogin.pickled_login(driver)

# a = HomePage(driver)
# b = ShowToolsPage(driver)

# driver.get('https://netflix.com/browse')
# driver.execute_script("window.scrollTo(0, 10000000)")

# a.scroll_to_bottom_of_page()

# a.get_random_row()

# l1 = driver.find_element(*a.SMALL_LOADING_CARD)
# l1.is_displayed()




# con = b.is_in_my_list_from_show_preview

# # print(a.get_random_row().text)
# print(a.get_random_show(a.get_random_row()).text)

# a.get_semi_random_show(condition=con)
# sho = a.get_totally_random_show()
# print(sho.text)
# # is_downvoted_from_show_preview


class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        # LOCATORS
        # MAIN BILLBOARD LOCATORS
        self.BILLBOARD_PLAY_BUTTON = (By.CSS_SELECTOR, 'div.billboard-row  a.playLink')
        self.MORE_INFO_BUTTON = (By.CSS_SELECTOR, 'a[data-uia="play-button"] + a')
        # ROW OPERATORS LOCATORS
        self.ALL_ROWS = (By.CSS_SELECTOR, 'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card')
        self.QUEUE_ROW = (By.CSS_SELECTOR, 'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card[data-list-context="queue"]')
        self.GENRE_ROWS = (By.CSS_SELECTOR, 'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card[data-list-context="genre"]')
        self.CONTINUE_WATCHING_ROW = (By.CSS_SELECTOR, 'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card[data-list-context="continueWatching"]')
        self.TRENDING_NOW_ROW = (By.CSS_SELECTOR, 'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card[data-list-context="trendingNow"]')
        self.SIMILARS_ROWS= (By.CSS_SELECTOR, 'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card[data-list-context="similars"]')
        self.BECAUSE_YOU_ADDED_ROWS = (By.CSS_SELECTOR, 'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card[data-list-context="becauseYouAdded"]')
        self.NEW_RELEASE_ROWS = (By.CSS_SELECTOR, 'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card[data-list-context="newRelease"]')
        self.TOP_TEN_ROWS = (By.CSS_SELECTOR, 'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card[data-list-context="topTen"]')
        self.NETFLIX_ORIGINALS_ROWS = (By.CSS_SELECTOR, 'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card[data-list-context="netflixOriginals"]')
        self.POPULAR_TITLES_ROWS = (By.CSS_SELECTOR, 'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card[data-list-context="popularTitles"]')
        self.BIG_ROW_ROWS = (By.CSS_SELECTOR, 'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card[data-list-context="bigRow"]')
        self.MOST_WATCHED_ROWS = (By.CSS_SELECTOR, 'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card[data-list-context="mostWatched"]')
        #########
        self.ROW_TITLE = (By.CSS_SELECTOR, 'a.rowTitle')
        self.RIGHT_CHEVRON = (By.CSS_SELECTOR, 'span.handle.handleNext.active')
        self.LEFT_CHEVRON = (By.CSS_SELECTOR, 'span.handle.handlePrev.active')
        ###########
        self.SHOW_ELEMENTS = (By.CSS_SELECTOR, 'a[class="slider-refocus"]')
        self.HOME_BUTTON = (By.CSS_SELECTOR, 'a[aria-label="Netflix"]')
        self.SMALL_LOADING_CARD = (By.CSS_SELECTOR, 'div.smallTitleCard.loadingTitle')
        self.LOADING_ROW = (By.CSS_SELECTOR, 'div.lolomoRow.lolomoRow_title_card.lolomoPreview')


    def scroll_to_top_of_page(self):
        """Scroll to the top of the page."""
        self.driver.execute_script("window.scrollTo(0, 0)")

    def scroll_to_bottom_of_page(self):
        """Scroll to the botom of the page."""
        # THIS LOADS EVERY SINGLE ROW AND TAKES ABOUT 9 SECONDS TO FINISH
        print(f"script started at {time.time()}")
        self.driver.execute_script("window.scrollTo(0, 10000000)")

        small_loading_card = self.driver.find_element(*self.SMALL_LOADING_CARD)

        # wait = WebDriverWait(self.driver, 10)
        # wait.until(EC.visibility_of_element_located(self.SMALL_LOADING_CARD))

        # Wait for all the placeholder loading cards to disappear
        wait = WebDriverWait(self.driver, 15)
        wait.until(EC.staleness_of(small_loading_card))
        print(f"finished loading script at {time.time()}")

    # ROW OPERATIONS
    def get_queue_row(self):
        """Return the queue_row/my-list_row in the proper row_element format."""
        q_row = self.driver.find_element(*self.QUEUE_ROW)
        return q_row

    def get_genre_rows(self) -> list:
        """Return a list of genre_rows in the proper row_element format."""
        # the first paint doesnt include a genre row, need to wait for one to load
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located(self.GENRE_ROWS))

        all_genre_rows = self.driver.find_elements(*self.GENRE_ROWS)
        return all_genre_rows

    def get_continue_watching_row(self):
        """Return the continue_watching_row in the proper row_element format."""
        continue_watching_row = self.driver.find_element(*self.CONTINUE_WATCHING_ROW)
        return continue_watching_row

    def get_trending_now_row(self):
        """Return the trending_now_row in the proper row_element format."""
        trending_now_row = self.driver.find_element(*self.TRENDING_NOW_ROW)
        return trending_now_row

    def get_similars_rows(self) -> list:
        """Return a list of  similars_rows in the proper row_element format."""
        # These are rows that are targeted at the profile
        similars_rows = self.driver.find_elements(*self.SIMILARS_ROWS)
        return similars_rows

    def get_because_you_added_rows(self) -> list:
        """Return a list of because_you_added_rows in the proper row_element format."""
        because_you_added_rows = self.driver.find_elements(*self.BECAUSE_YOU_ADDED_ROWS)
        return because_you_added_rows

    def get_new_release_rows(self) -> list:
        """Return a list of new_release_rows in the proper row_element format."""
        new_release_rows = self.driver.find_elements(*self.NEW_RELEASE_ROWS)
        return new_release_rows

    def get_top_ten_rows(self) -> list:
        """Return a list of top_ten_rows in the proper row_element format."""
        top_ten_rows = self.driver.find_elements(*self.TOP_TEN_ROWS)
        return top_ten_rows

    def get_netflix_originals_rows(self) -> list:
        """Return a list of netfli_originals_rows in the proper row_element format."""
        netflix_originals_rows = self.driver.find_elements(*self.NETFLIX_ORIGINALS_ROWS)
        return netflix_originals_rows

    def get_popular_titles_rows(self) -> list:
        """Return a list of popular_titles_rows in the proper row_element format."""
        popular_titles_rows = self.driver.find_elements(*self.POPULAR_TITLES_ROWS)
        return popular_titles_rows

    def get_big_row_rows(self) -> list:
        """Return a list of big_row_rows in the proper row_element format."""
        big_row_rows = self.driver.find_elements(*self.BIG_ROW_ROWS)
        return big_row_rows

    def get_most_watched_rows(self) -> list:
        """Return a list of most_watched_rows in the proper row_element format."""
        most_watched_rows = self.driver.find_elements(*self.MOST_WATCHED_ROWS)
        return most_watched_rows

    #######################################################################################

    def row_page_right(self, row_element):
        """Take in the row_element and click the chevron right to see the next page of shows."""
        first_show = self.get_first_show_in_row(row_element)  # grabbing a show to facilitate wait

        right_chevron = row_element.find_element(*self.RIGHT_CHEVRON)
        right_chevron.click()

        # waiting for the row to change by waiting for the staleness of the first show in the row
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.staleness_of(first_show))

    def row_page_left(self, row_element):
        """Take in the row_element and click the chevron left to see the previous page of shows."""
        # Left doesnt exist for some rows until right is clicked once (and thus there is something
        # to go left to)
        first_show = self.get_first_show_in_row(row_element)  # grabbing a show to facilitate wait
        try:
            left_chevron = row_element.find_element(*self.LEFT_CHEVRON)
            left_chevron.click()
        except NoSuchElementException:
            print("row_page_left couldnt find left chevron. Did you row_page_right first?")

        # waiting for the row to change by waiting for the staleness of the first show in the row
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.staleness_of(first_show))

    def get_recommended_genres(self) -> list:
        """Return a list of genres displayed on the home page. Different for every user."""
        # SCROLL TO THE BUTTOM OF THE HOME PAGE
        # 10 lazy loads by netflix. Have to scroll to the bottom, then more loads
        # repeat 10 times
        for i in range(10):
            self.driver.execute_script("window.scrollTo(0, 10000000)")
            print(i)
            # removed a sleep here, add a wait if necessary
        genre_rows = self.get_genre_rows(self)
        genres = [genre.text for genre in genre_rows]
        return genres

    ####################################################################################
    # NOTE TO READER. ANY FUNCTIONS RELATED TO INTERACTING WITH SHOW ELEMNTS CAN BE FOUND IN
    # showtools.py. THE FOLLOWING FUCNTIONS FALL IN THE DOMAIN OF ROW_ELEMENT FUCNTIONS
    def get_show_titles_from_row(self, row_element):
        """This one is complicated. Netflix's frontend doesnt populate the DOM with all of the
        shows. the test suite needs to force all of the shows to load by using get_page_right().
        """
        final_show_titles_list = []
        for _ in range(20):  # 20 is an arbitrary number. TODO- Find the max number
            currently_displayed_shows = self.get_currently_displayed_in_row(row_element)
            current_titles = [
                show.text
                for show in currently_displayed_shows
                if show.text not in final_show_titles_list
            ]
            if not current_titles:
                # No new titles were found
                break
            else:
                final_show_titles_list += current_titles
                self.row_page_right(row_element)
        return final_show_titles_list

    def get_currently_displayed_in_row(self, row_element):
        """Return a list of show elements that are actively displayed in row_element. Actively
        displayed implies visible to the naked eye."""
        slider_items = row_element.find_elements_by_css_selector('div.slider-item')
        # print(f"found {len(slider_items)} slider items")
        currently_displayed_shows = []  # LIST OF SHOW_ELEMENTS, NOT TITLES

        for item in slider_items:
            try:
                show_a_tag = item.find_element_by_css_selector('div > div > div > a')
                # print(show_a_tag.get_attribute('aria-hidden'))
                if show_a_tag.get_attribute('aria-hidden') == 'false':
                    # CAN NOT JUST ADD show_a_tag TO A LIST. NEED TO CONFORM TO SHOW_ELEMENT OBJECT
                    new_show_element = item.find_element(*self.SHOW_ELEMENTS)
                    currently_displayed_shows.append(new_show_element)
            except NoSuchElementException:
                continue
        return currently_displayed_shows

    def get_first_show_in_row(self, row_element):
        """Return the first show_element, in proper format, in the row row_element."""
        return self.get_currently_displayed_in_row(row_element)[0]

    def get_random_row(self):
        """Return a random row that contains standard show elements. (excludes my-list, big-row,
        topTen, etc.)"""

        all_rows = self.driver.find_elements(*self.ALL_ROWS)

        desired_rows = [
            row for row in all_rows
            if row.get_attribute('data-list-context') in
            ['genre', 'popularTitles', 'trendingNow', 'similars', 'becauseYouAdded']
        ]
        print(f"get_random_row found {len(desired_rows)} rows to choose from")
        return random.choice(desired_rows)

    def get_semi_random_show(self, row_element=None, condition=None, condition_bool=None):
        """ CONDITION MUST BE A BOBCONTAINER FUCNTION e.g. is_in_my_list, is_upvoted"""
        show_tools = pagemodels.showtoolspage.ShowToolsPage(self.driver)

        if condition_bool.lower() == 'true':
            raise Exception("get_semi_random_show param condition_bool is either False or None")

        # We need to scroll to the bottom of the page to generate more shows to increase randomness
        # self.scroll_to_bottom_of_page()

        # get a list of random shows from a random row or row_element if specified
        if not row_element:
            random_row = self.get_random_row()
            show_choices = self.get_currently_displayed_in_row(random_row)
            print(f"found {len(show_choices)} shows in a random row")
        if row_element:
            show_choices = self.get_currently_displayed_in_row(row_element)
            print(f"found {len(show_choices)} in the specified row")

        random.shuffle(show_choices)

        if not condition:
            # if no condition is passed in, return any random show
            return show_choices[0]
        elif condition and condition_bool:
            if condition_bool.lower() == 'false':
                # find a show where the condition IS FALSE
                for show in show_choices:
                    print("gate 1")
                    print(show.text)
                    if not condition(show):
                        return show
                    else:
                        home_button = self.driver.find_element(*self.HOME_BUTTON)
                        bob_play_hitzone = self.driver.find_element(*show_tools.BOB_PLAY_HITZONE)

                        action = ActionChains(self.driver)
                        action.move_to_element(home_button).perform()

                        wait = WebDriverWait(self.driver, 10)
                        wait.until(EC.invisibility_of_element_located(bob_play_hitzone))
        else:
            # find a show that where condition is TRUE
            for show in show_choices:
                # find a show where the condition is true
                print("gate 1")
                print(show.text)
                if condition(show):
                    return show
                else:
                    home_button = self.driver.find_element(*self.HOME_BUTTON)
                    bob_play_hitzone = self.driver.find_element(*show_tools.BOB_PLAY_HITZONE)

                    action = ActionChains(self.driver)
                    action.move_to_element(home_button).perform()

                    wait = WebDriverWait(self.driver, 10)
                    wait.until(EC.invisibility_of_element_located(bob_play_hitzone))

        # Improbable edge case where a random genre will show a bunch of shows, all of
        # which did not satisfy condition & condition_bool
        raise Exception("get_semi_random_show FAILED TO FIND A RANDOM SHOW")

    def get_totally_random_show(self):
        """Get a random show that is currently displayed on the homepage."""
        # May or may not be in my list, upvoted, downvoted
        # BUG- RETURNING NOT SHOW ELEMENTS SOMETIMES, show.text is printing ''
        # I dont think all

        all_shows = self.driver.find_elements(*self.SHOW_ELEMENTS)
        print(f"get_totally_random_show found {len(all_shows)} shows")

        return random.choice(all_shows)


