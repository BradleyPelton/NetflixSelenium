from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pagemodels.basepage import BasePage


# The Home page for netflix is netflix.com/browse. Everything leads back to /browse somehow

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

    def get_queue_row(self):
        """ TODO- UNTESTED"""
        q_row = self.driver.find_element(*self.QUEUE_ROW)
        return q_row

    def get_genre_rows(self) -> list:
        """ TODO- UNTESTED"""
        all_genre_rows = self.driver.find_element(*self.GENRE_ROWS)
        return all_genre_rows

    def get_continue_watching_row(self):
        """TODO- UNTESTED"""
        continue_watching_row = self.driver.find_element(*self.CONTINUE_WATCHING_ROW)
        return continue_watching_row

    def get_trending_now_row(self):
        """TODO- UNTESTED"""
        trending_now_row = self.driver.find_element(*self.TRENDING_NOW_ROW)
        return trending_now_row

