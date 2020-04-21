# from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.action_chains import ActionChains

from pagemodels.basepage import BasePage
# import tests.pickledlogin
# import secrets

###########################################################################################
###########################################################################################
###########################################################################################
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= HEADER FUNCTIONS =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#  THE FOLLOWING FUNCTIONS ARE NOT SPECIFIC TO THE HOMEPAGE. ALL PAGES HAVE ACCESS TO THIS HEADER
# AND THUS ALL OF THESE FUNCIONS. ENOUGH FUCNTIONS WARRANT A STAND ALONE PAGE
###########################################################################################
###########################################################################################
###########################################################################################


class HeaderPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        # Locators
        self.HOME_BUTTON = (By.CSS_SELECTOR, 'a[aria-label="Netflix"]')
        self.ACCOUNT_DROPDOWN_BUTTON = (By.CSS_SELECTOR, 'div.account-dropdown-button')
        self.DROPDOWN_OPTIONS = (By.CSS_SELECTOR, 'ul.account-links.sub-menu-list > li')
        self.MANAGE_PROFILES_BUTTON = (By.CSS_SELECTOR, 'a[aria-label="Manage Profiles"]')
        self.NOTIFICATION_MENU_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Notifications"]')
        self.NOTIFICATIONS_CONTAINER = (By.CSS_SELECTOR, 'ul.notifications-container')
        self.NOTIFICATIONS = (By.CSS_SELECTOR, 'ul.notifications-container div > li.notification')
        self.SEARCH_FIELD = (By.CSS_SELECTOR, 'input[data-uia="search-box-input"]')
        self.SEARCH_BUTTON = (By.CSS_SELECTOR, 'button.searchTab')
        self.SHOW_ELEMENTS = (By.CSS_SELECTOR, 'a[class="slider-refocus"]')

    def logout(self):
        """From the account dropdown in the header, logout."""
        account_dropdown_button = self.driver.find_element(*self.ACCOUNT_DROPDOWN_BUTTON)
        account_dropdown_button.click()

        dropdown_options = self.driver.find_elements(*self.DROPDOWN_OPTIONS)

        logout_button = dropdown_options[2]
        logout_button.click()

    def navigate_to_home(self):
        """Navigate home using the home button in the top left corner of the header."""
        home_button = self.driver.find_element(*self.HOME_BUTTON)
        home_button.click()

    def navigate_to_manage_profile(self):
        """Navigate to the manage profiles page, https://www.netflix.com/profiles/manage, by
        clicking on the manage profiles button from the account dropdown in the header.
        """
        account_dropdown_button = self.driver.find_element(*self.ACCOUNT_DROPDOWN_BUTTON)
        account_dropdown_button.click()

        manage_profiles_button = self.driver.find_element(*self.MANAGE_PROFILES_BUTTON)
        manage_profiles_button.click()

    def clear_notifications(self):
        """Clear notifications by opening the notifications dropdown and then closing it."""
        notifications_menu_button = self.driver.find_element(*self.NOTIFICATION_MENU_BUTTON)
        notifications_menu_button.click()
        notifications_menu_button.click()

    def click_top_notification(self):
        """Click the top notification form the notification dropdown in the header."""
        notifications_menu_button = self.driver.find_element(*self.NOTIFICATION_MENU_BUTTON)
        notifications_menu_button.click()

        notifications = self.driver.find_elements(*self.NOTIFICATIONS)

        top_notification = notifications[0]
        top_notification.click()

        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.staleness_of(top_notification))

    def search_field_is_open(self) -> bool:
        """Return true if the search field is open, false if else."""
        # Netflix's serach field doesnt appear until the user clicks the search button.
        try:
            self.driver.find_element(*self.SEARCH_FIELD)
            return True
        except NoSuchElementException:
            return False

    def clear_search(self):
        """Clear the search field as seen from the header."""
        search_field = self.driver.find_element(*self.SEARCH_FIELD)
        search_field.clear()

    def search(self, search_term: str):
        """Search for 'search_term' show in Netflix by using the search field."""
        if self.search_field_is_open():
            self.clear_search()
        else:
            search_button = self.driver.find_element(*self.SEARCH_BUTTON)
            search_button.click()

        search_field = self.driver.find_element(*self.SEARCH_FIELD)
        # search_field.send_keys(search_term)

        # old idea: one key stroke at a time with some added waits to represent "think time"
        # pass one character in at a time to better simulate user activity
        for char in search_term:
            search_field.send_keys(char)

        # wait until the first show is displayed after the search
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located(self.SHOW_ELEMENTS))

    # def click_refer_button(driver):
    #     """ waste of time. adding it here just for completeness"""
    #     pass
