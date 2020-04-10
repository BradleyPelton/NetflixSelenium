from collections import defaultdict

from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pagemodels.basepage import BasePage

# MOVIES AND SHOWS HAVE HIDDEN GENRES AND PUBLIC GENRES
# A PUBLIC GENRE IS SOMETHING LIKE "ROMANCE", "ACTION", "HORROR"
# A HIDDEN GENRE IS AN UNDISCLOSED ID ASSIGNED BY NETFLIX AND DISPLAYED IN THE URL
# E.G https://www.netflix.com/browse/genre/83 FOR "Tv Shows"

# TODO- There are three other sort methods: Suggested for you, Z-A, Year Released
# CREATE FUCNTIONS FOR EACH OF THESE


class GenrePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        # Locators
        self.GRID_BUTTON = (By.CSS_SELECTOR, 'button.aro-grid-toggle')
        self.SORT_DROPDOWN = (By.CSS_SELECTOR, 'div.nfDropDown.widthRestricted.theme-aro')
        self.ALPHA_SORT = (By.CSS_SELECTOR, 'div.sub-menu.theme-aro > ul > li:nth-child(3)')
        self.SHOWS = (By.CSS_SELECTOR, 'a[class="slider-refocus"]')
        self.JAWBONE_CLOSE_BUTTON = (By.CSS_SELECTOR, 'button.close-button.icon-close')

    def switch_to_grid(self):
        """ switch from the default row display( that scroll right to display more)
        to the grid view pattern by clicking the grid pattern button
        """
        grid_button = self.driver.find_element(*self.GRID_BUTTON)
        grid_button.click()

    def switch_to_alpha_sort(self):
        """click the dropdown that allows user to change the sort method
        change the sort method to alpha
        """
        sort_dropdown = self.driver.find_element(*self.SORT_DROPDOWN)
        sort_dropdown.click()

        alpha_sort = self.driver.find_element(*self.ALPHA_SORT)
        alpha_sort.click()
        # current_sort_option = driver.find_element_by_css_selector(
        # 'div.nfDropDown.widthRestricted.theme-aro > div')
        # print(f"Currently sourting by {current_sort_option.text}")

    def master_sweep(self, genre_id: int) -> dict:
        """ MASTER SWEEP  TODO- GENERALIZE, STILL USES ANIME NAMES"""
        self.driver.get("https://www.netflix.com/browse/genre/" + str(genre_id))
        self.switch_to_grid()
        self.switch_to_alpha_sort()

        shows = self.driver.find_element(*self.SHOWS)

        anime_shows_dict = defaultdict(dict)
        for show in shows[0:10]:
            title = show.text
            anime_shows_dict[title] = {}  # add show titles
            # OPEN JAWBONE
            show.click()
            # Let jawbone load, explicit wait until jawbone is open
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.meta-lists')))

            if self.show_has_saved_progress(self.driver, show, JAWBONE_OPEN=True):
                anime_shows_dict[title]['progress'] = 'T'
            else:
                anime_shows_dict[title]['progress'] = 'F'

            if mylisttools.is_in_my_list(driver, show, JAWBONE_OPEN=True):
                anime_shows_dict[title]['is_in_my_list'] = 'T'
            else:
                anime_shows_dict[title]['is_in_my_list'] = 'F'

            anime_shows_dict[title]['actors'] = self.get_actors_list(
                self.driver, show, JAWBONE_OPEN=True)
            anime_shows_dict[title]['genres'] = self.get_genre_list(
                self.driver, show, JAWBONE_OPEN=True)
            anime_shows_dict[title]['tags'] = self.get_tags_list(
                self.driver, show, JAWBONE_OPEN=True)

            jawBone_close_button = self.driver.find_element(*self.JAWBONE_CLOSE_BUTTON)
            jawBone_close_button.click()

            # explicitly waiting until jawbone is closed
            wait.until(EC.invisibility_of_element_located(jawBone_close_button))



