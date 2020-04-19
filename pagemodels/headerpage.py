import time

# from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
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

# chromedriver_path = secrets.chromedriver_path
# driver = webdriver.Chrome(executable_path=chromedriver_path)
# tests.pickledlogin.pickled_login(driver)

# a = HeaderPage(driver)
# a.logout()

# b = driver.find_element_by_css_selector('a[aria-label="Netflix"]')


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
        self.SEARCH_FIELD = (By.CSS_SELECTOR, 'input[data-uia="search-box-input"]')
        self.SEARCH_BUTTON = (By.CSS_SELECTOR, 'button.searchTab')

    def logout(self):
        """ self explanatory, tested"""
        account_dropdown_button = self.driver.find_element(*self.ACCOUNT_DROPDOWN_BUTTON)
        account_dropdown_button.click()

        dropdown_options = self.driver.find_elements(*self.DROPDOWN_OPTIONS)

        logout_button = dropdown_options[2]
        logout_button.click()

    def navigate_to_home(self):
        """ navigate home using the home button in the top left corner """
        home_button = self.driver.find_element(*self.HOME_BUTTON)
        home_button.click()

    def navigate_to_manage_profile(self):
        """ navigate to the manage profiles page, https://www.netflix.com/profiles/manage, by clicking
        on the manage profiles button from the account dropdown from the header
        """
        """ NOTE- while these functions contribute to completeness by testing individual buttons, it
        is much more important to test key features in the first version of the automation suite"""
        account_dropdown_button = self.driver.find_element(*self.ACCOUNT_DROPDOWN_BUTTON)
        account_dropdown_button.click()

        manage_profiles_button = self.driver.find_element(*self.MANAGE_PROFILES_BUTTON)
        manage_profiles_button.click()

    def clear_notifications(self):
        """ CLEAR NOTIFICATIONS BY OPENING THE NOTIFICATIONS DROPDOWN AND THEN CLOSING IT"""
        """ TODO- NEED NOTIFIATIONS TO APPEAR AGAIN TO TEST. TODO"""
        notifications_menu_button = self.driver.find_element(*self.NOTIFICATION_MENU_BUTTON)
        notifications_menu_button.click()
        notifications_menu_button.click()

    def click_top_notification(self):
        """ self-explanatory. Works from every non-video page"""
        notifications_menu_button = self.driver.find_element(*self.NOTIFICATION_MENU_BUTTON)
        notifications_menu_button.click()

        notifications_container = self.driver.find_element(*self.NOTIFICATIONS_CONTAINER)
        notifications = notifications_container.find_elements_by_css_selector(
            'div > li.notification')

        top_notification = notifications[0]
        top_notification.click()

    def search_field_is_open(self) -> bool:
        """ return True if the search field is open, False if else"""
        try:
            self.driver.find_element(*self.SEARCH_FIELD)
            return True
        except NoSuchElementException:
            return False

    def clear_search(self):
        """ search field is non-empty IFF it is open. Thus we dont have to open the search field
        here"""
        search_field = self.driver.find_element(*self.SEARCH_FIELD)
        search_field.clear()

    def search(self, search_term: str):
        """ uses the search bar in the header to search for search_term"""
        """ TODO- This is a exactly what a serach is in theory, but in practice, Netflix handles
        a little differently. Notice when searching things manually, the netflix app actually
        searches after EVERY SINGLE key press. Thus if we were to search for "Top Gun" manually,
        the observerwill notice that 7 DIFFERENT page results are displayed in the results
        (len("Top Gun")). This is the fundamental difference between automation testing and
        automating user behavior. We needto actually mimic user behavior. In this case the 2 differ
        because Selenium.send_keys() sends all of the keys at the same time.
        TODO- THIS IS GOOD THEORY. GOOD DISCUSSION. READDD MEEEE"""
        if self.search_field_is_open():
            self.clear_search()
        else:
            # TODO- Turn open_seach_field into a function??? Seems a little verbose
            search_button = self.driver.find_element(*self.SEARCH_BUTTON)
            search_button.click()
        search_field = self.driver.find_element(*self.SEARCH_FIELD)
        search_field.send_keys(search_term)

        # let the results load
        time.sleep(3)

    # def click_refer_button(driver):
    #     """ waste of time. adding it here just for completeness"""
    #     pass
