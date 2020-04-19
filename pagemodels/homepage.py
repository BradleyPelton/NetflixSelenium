import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


from pagemodels.basepage import BasePage
import secrets
import pagemodels.showtoolspage
import tests.pickledlogin


# The Home page for netflix is netflix.com/browse. Everything leads back to /browse somehow

# RECALL A show_element HAS A VERY SPECIFIC FORMAT. THE NODE HAS TO BE AN A TAG LOCATED INSIDER
# 'div.slider-item > div > div > a.slider-refocus'

# # # DELETE ME
# chromedriver_path = secrets.chromedriver_path
# driver = webdriver.Chrome(executable_path=chromedriver_path)
# tests.pickledlogin.pickled_login(driver)

# a = HomePage(driver)
# b = ShowToolsPage(driver)

# que = a.get_queue_row()
# first_show = a.get_first_show_in_row(que)
# print(first_show.text)

# gen_rows = a.get_genre_rows()
# first_row = gen_rows[0]
# first_show = a.get_first_show_in_row(first_row)
# print(first_show.text)

# b.mouse_over_show_element(first_show)
# b.show_is_being_previewed()
# b.mouse_over_show_if_not_moused_over(first_show)
# b.is_upvoted_from_jawbone(first_show)
# b.is_downvoted_from_jawbone(first_show)
# b.upvote_from_jawbone(first_show)
# b.close_jawbone()
# b.downvote_from_jawbone(first_show)
# b.remove_downvote_or_upvote_from_jawbone(first_show)

# COOL HIGHLIST FUCNTION FOR DEBUGGING
# def highlight(element):
#     """Highlights (blinks) a Selenium Webdriver element"""
#     driver = element._parent
#     def apply_style(s):
#         driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
#                               element, s)
#     original_style = element.get_attribute('style')
#     apply_style("background: yellow; border: 2px solid red;")
#     time.sleep(.3)
#     apply_style(original_style)

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        # LOCATORS
        # MAIN BILLBOARD LOCATORS
        self.BILLBOARD_PLAY_BUTTON = (By.CSS_SELECTOR, 'div.billboard-row  a.playLink')
        self.MORE_INFO_BUTTON = (By.CSS_SELECTOR, 'a[data-uia="play-button"] + a')
        # ROW OPERATORS LOCATORS
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
        self.LEFT_CHEVRON = (By.CSS_SELECTOR, 'span.handle.handlePrev.active' )
        ###########
        self.SHOW_ELEMENTS = (By.CSS_SELECTOR, 'a[class="slider-refocus"]')

    def scroll_to_top_of_page(self):
        self.driver.execute_script("window.scrollTo(0, 0)")

    def scroll_to_bottom_of_page(self):
        self.driver.execute_script("window.scrollTo(0, 10000000)")

    # ROW OPERATIONS
    def get_queue_row(self):
        """ TODO- UNTESTED"""
        q_row = self.driver.find_element(*self.QUEUE_ROW)
        return q_row

    def get_genre_rows(self) -> list:
        """ TODO- UNTESTED"""
        all_genre_rows = self.driver.find_elements(*self.GENRE_ROWS)
        return all_genre_rows

    def get_continue_watching_row(self):
        """TODO- UNTESTED"""
        continue_watching_row = self.driver.find_element(*self.CONTINUE_WATCHING_ROW)
        return continue_watching_row

    def get_trending_now_row(self):
        """TODO- UNTESTED"""
        trending_now_row = self.driver.find_element(*self.TRENDING_NOW_ROW)
        return trending_now_row

    def get_similars_rows(self) -> list:
        """ These are rows that are targeted at the profile"""
        similars_rows = self.driver.find_elements(*self.SIMILARS_ROWS)
        return similars_rows

    def get_because_you_added_rows(self) -> list:
        """ BUG- see get_row_titles_from_row_list"""
        """rows with data-list-context="becauseYouAdded". These rows are targetd at the profile based
        on the user having added the show the row is named after (e.g. Because you Added Top Gun)
        """
        because_you_added_rows = self.driver.find_elements(*self.BECAUSE_YOU_ADDED_ROWS)
        return because_you_added_rows

    def get_new_release_rows(self) -> list:
        """ TODO"""
        new_release_rows = self.driver.find_elements(*self.NEW_RELEASE_ROWS)
        return new_release_rows

    def get_top_ten_rows(self) -> list:
        """ row? rows? TODO find out"""
        """ TODO"""
        top_ten_rows = self.driver.find_elements(*self.TOP_TEN_ROWS)
        return top_ten_rows

    def get_netflix_originals_rows(self) -> list:
        """ row? rows? TODO find out"""
        """ TODO"""
        netflix_originals_rows = self.driver.find_elements(*self.NETFLIX_ORIGINALS_ROWS)
        return netflix_originals_rows

    def get_popular_titles_rows(self) -> list:
        """ row? rows? TODO find out"""
        popular_titles_rows = self.driver.find_elements(*self.POPULAR_TITLES_ROWS)
        return popular_titles_rows

    def get_big_row_rows(self) -> list:
        """ row? rows? TODO find out"""
        """ TODO"""
        big_row_rows = self.driver.find_elements(*self.BIG_ROW_ROWS)
        return big_row_rows

    def get_most_watched_rows(self) -> list:
        """ row? rows? TODO find out"""
        """ TODO"""
        most_watched_rows = self.driver.find_elements(*self.MOST_WATCHED_ROWS)
        return most_watched_rows

    #######################################################################################

    def get_row_titles_from_row_list(self, row_list: list) -> list:
        """
            TODO-INTENDED FOR A LIST OF ROWS, NOW A SINGLE ROW
        INPUT: list of WEBELEMENTS of row elements (div.lolomoRow.lolomoRow_title_card)
            OUTPUT: THE LIST OF TITLES FOR THOSE ROW ELEMENTS
        """
        # THIS FUNC
        # BUG- TODO- for some reason, get_becauseYouAdded_rows have the title stored in
        # a span.rowTitle
        # instead of a.rowTitle.  FIX BUG TODO Investigate other rows
        row_title_list = []
        for row in row_list:
            row_title = row.find_element(*self.ROW_TITLE)
            # print(row_title.text)
            row_title_list.append(row_title.text)
        return row_title_list

    def row_page_right(self, row_element):
        """take in the row_element and click the chevron right to see the next page of shows"""
        right_chevron = row_element.find_element(*self.RIGHT_CHEVRON)
        right_chevron.click()
        # BUG- SOMETIMES I CANT PAGE RIGHT. ElementClickInterceptedException

    def row_page_left(self, row_element):
        """take in the row_element and click the chevron left to see the previous page of shows.
        LEFTDOESNT EXIST FOR SOME ROWS UNTIL RIGHT IS CLICKED ONCE (and thus there is something to
        go left)
        """
        left_chevron = row_element.find_element(*self.LEFT_CHEVRON)
        left_chevron.click()

    def get_recommended_genres(self) -> list:
        """TODO """
        # SCROLL TO THE BUTTOM OF THE HOME PAGE
        # 10 lazy loads by netflix. Have to scroll to the bottom, then more loads
        # repeat 10 times
        for i in range(10):
            self.driver.execute_script("window.scrollTo(0, 10000000)")
            print(i)
            time.sleep(1)  # TODO- SLOPPY TO USE TIME. REFACTOR

        genre_rows = self.get_genre_rows(self)
        genres = [genre.text for genre in genre_rows]
        return genres

    #####################################################################################
    # NOTE TO READER. ANY FUNCTIONS RELATED TO INTERACTING WITH SHOW ELEMNTS CAN BE FOUND IN
    # showtools.py. THE FOLLOWING FUCNTIONS ARE SQUARELY IN THE DOMAIN OF ROW_ELEMENT FUCNTIONS
    def get_show_titles_from_row(self, row_element):
        """ this one is complicated. Netflix's frontend doesnt populate the DOM with all of the
        shows. the test suite needs to force all of the shows to load by using get_page_right()
        Even worse yet, the last row is populated with the elements of the first row if the last
        row doent fill the entire row. EEEEVEEEENNNNN WORSE YET, the number of shows displayed
        varies on the size of the screen. TODO- SLOW AND HIDEOUS, BUT FUNCTIONAL
        """
        # Note from/to author: This is not a data scraping job. This is a test suite
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
                time.sleep(1)  # Sloppy work to use SLEEP TODO- CLEAN
        return final_show_titles_list

    def get_first_show_in_row(self, row_element):
        """ return a show_element. NOTE- SHOW ELEMENTS ARE JUST AS SPECIAL AS ROW_ELEMNTS. THIS
        TEST SUITE CONSIDERS THE TWO TO BE FUNDAMENTAL. THUS THE SHOW_ELEMENT MUST FIT THE
        STANDARDS, i.e. show = driver.find_elements_by_css_selector('a[class="slider-refocus"]')
        """
        # TODO- NOTE- TODO

        return self.get_currently_displayed_in_row(row_element)[0]

    def get_currently_displayed_in_row(self, row_element):
        """ return a list of show elements THAT ARE ACTIVELY DISPLAYED IN ROW. BY ACTIVEL DISPLAYED
        I MEAN VISIBLE TO THE NAKED EYE"""

        slider_items = row_element.find_elements_by_css_selector('div.slider-item')
        # print(f"found {len(slider_items)} slider items")
        currently_displayed_shows = []  # LIST OF SHOW_ELEMENTS, NOT TITLES

        for item in slider_items:
            try:
                temp = item.find_element_by_css_selector('div > div > div > a')
                # print(temp.get_attribute('aria-hidden'))
                if temp.get_attribute('aria-hidden') == 'false':
                    # CAN NOT JUST ADD TEMP TO A LIST. NEED TO CONFORM TO SHOW_ELEMENT OBJECT
                    new_show_element = item.find_element(*self.SHOW_ELEMENTS)
                    currently_displayed_shows.append(new_show_element)
            except NoSuchElementException:
                continue
        return currently_displayed_shows
