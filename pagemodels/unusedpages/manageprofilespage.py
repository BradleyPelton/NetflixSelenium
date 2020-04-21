
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from pagemodels.basepage import BasePage

#########################################################################
# MANAGE PROFILES IS NOT THE SAME THING AS SELECT PROFILE
# WHEN A USER LOGS INTO NETFLIX, THEY ARE ASKED TO SELECT A PROFILE
# DO NOT CONFUSE THE TWO
#########################################################################


########################################################################################
########################################################################################
# THIS PAGE IS NOT CURRENTLY SUPPORTED. YOUR RESULTS MAY VARY
########################################################################################
########################################################################################


class ManageProfilesPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        # Locators
        self.PROFILES = (By.CSS_SELECTOR, 'ul.choose-profile > li')
        self.EDIT_PROFILE_CONTAINER = (By.CSS_SELECTOR, 'div.profile-edit-inputs > input')
        self.AVATAR_WRAPPER = (By.CSS_SELECTOR, 'div.avatar-wrapper')
        self.ADD_PROFILE_BUTTON = (By.CSS_SELECTOR, 'div.addProfileIcon.icon-tvuiAdd')
        self.PROFILE_NAME_FIELD = (By.CSS_SELECTOR, 'input[id="add-profile-name"]')


        
        # DUPLICATE. KIDS_CHECKBOX VS CHECKBOX_KIDS TODO BECAREFUL
        self.KIDS_CHECKBOX = (By.CSS_SELECTOR, 'div.add-kids-option')
        self.TEENS_CHECKBOX = (By.CSS_SELECTOR, 'div.add-teen-option')



        self.CONTINUE_BUTTON = (By.CSS_SELECTOR, 'span.profile-button.preferred-action.preferred-active')
        self.DELETE_BUTTON = (By.CSS_SELECTOR, 'span[data-uia="profile-delete-button"]')
        self.NAME_INPUT_FIELD = (By.CSS_SELECTOR, 'div.profile-edit-inputs > input')
        self.CHECKBOX_KIDS = (By.CSS_SELECTOR, 'label[for="add-kids-profile"]')
        self.CURRENT_LANGUAGE = (By.CSS_SELECTOR, 'a.user-lang-link')
        self.MATURITY_DROPDOWN = (By.CSS_SELECTOR, 'div[data-uia="maturity-drop-down"]')
        self.AUTOPLAY_EPISODES_CHECKBOX = (By.CSS_SELECTOR, 'label[for="nextEpisode-profile"]')
        self.AUTOPLAY_PREVIEWS_CHECKBOX = (By.CSS_SELECTOR, 'label[for="videomerch-profile"]')
        self.LANGUAGE_DROPDOWN = (By.CSS_SELECTOR, 'div.nfDropDown.theme-lakira > div')
        self.ENGLISH_CHOICE = (By.CSS_SELECTOR, 'div.sub-menu.theme-lakira > ul > li:nth-of-type(4)')
        self.SPANISH_CHOICE = (By.CSS_SELECTOR, 'div.sub-menu.theme-lakira > ul > li:nth-of-type(5)')




    def get_number_of_profiles(self) -> int:
        """ Netflix accounts can only have 5 different users.
        """
        profiles = self.driver.find_element(*self.PROFILES)
        number_of_profiles = len(
            [profile for profile in profiles if profile.text != "Add Profile"]
        )
        return number_of_profiles

    def get_profile_names(self) -> list:
        """ return the names of all of the profiles on this Netflix account"""
        profiles = self.driver.find_element(*self.PROFILES)
        profile_names = [profile.text for profile in profiles if profile.text != "Add Profile"]
        return profile_names

    def edit_profile_is_open(self) -> bool:
        """returns true if the edit profile modal is open, false if else"""
        try:
            self.driver.find_element(*self.EDIT_PROFILE_CONTAINER)
            return True
        except NoSuchElementException:
            return False

    def open_named_profile(self, profile_name):
        """ opens the profile with name: profile_name.
        https://www.netflix.com/ManageProfiles MUST BE OPEN """
        profiles = self.driver.find_element(*self.PROFILES)
        for profile in profiles:
            if profile.text == profile_name:
                avatar_wrapper = self.driver.find_element(*self.AVATAR_WRAPPER)
                avatar_wrapper.click()
                break
        # looping through 5 profiles is pretty trivial, but probably against Selenium good
        # practices. TODO- REFACTOR to find profile with an element that contains profile_name

        # wait for the profile to open
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located(self.DELETE_BUTTON))

    def create_new_profile(self, profile_name: str, for_kids=False, for_teens=False):
        """ for_kids or for_teens ARE MUTUALLY EXCLUSIVE, CAN'T BE BOTH"""
        if for_kids and for_teens:
            return("CREATE_NEW_PROFILE TEST IS BOMBINGOUT,CANT ACCEPT BOTH FOR_KIDS and FOR_TEENS")
        add_profile_button = self.driver.find_element(*self.ADD_PROFILE_BUTTON)
        add_profile_button.click()
        # Wait for the new profile creation modal to launch
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located(self.PROFILE_NAME_FIELD))
        name_field = self.driver.find_element(*self.PROFILE_NAME_FIELD)
        name_field.send_keys(profile_name)

        if for_kids:
            kids_checkbox = self.driver(*self.KIDS_CHECKBOX)
            kids_checkbox.click()
        if for_teens:
            teens_checkbox = self.driver.find_element(*self.TEENS_CHECKBOX)
            teens_checkbox.click()

        continue_button = self.driver.find_element(*self.CONTINUE_BUTTON)
        continue_button.click()

    def delete_profile(self, the_profile_name):
        """ TODO- CLEAN THIS UP. FILTHY"""
        """ opening and closing the edit modal will be handled elsewhere"""
        all_profile_names = self.get_profile_names()
        assert the_profile_name in all_profile_names, "Attempted to delete unknown profile"
        # refactor this, awkward and duplicate logic
        self.open_named_profile(the_profile_name)

        delete_button = self.driver.find_element(*self.DELETE_BUTTON)
        delete_button.click()
        # wait until deletion_confirmation dialogue appears
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'span.profile-button')))
        delete_profile_confirmation_button = driver.find_elements_by_css_selector('span.profile-button')[1]
        delete_profile_confirmation_button.click()
        # TODO- REFACTOR THIS FILTHY CODE

    def get_profile_settings(self) -> dict:
        """ opening and closing the edit modal will be handled elsewhere"""
        """ return a dictionary of the following settings:
        name: str
        kid?: bool
        current_language: str
        allowed_shows: str
        autoplay_episode: b
        ool
        autoplay_previews: bool
        """
        profile_settings = dict()

        name_field = self.driver.find_element(*self.NAME_INPUT_FIELD)
        profile_settings['name'] = name_field.get_attribute('value')

        kids_checkbox = self.driver.find_element(*self.CHECKBOX_KIDS)  # TODO- two checkbox CSS sel
        # IF THE CHECKBOX IS CHECKED, AN SVG CHILD ELEMENT IS CREATED.
        # THUS CHECKED IFF SVG CHILD EXISTS
        try:
            kids_checkbox.find_element_by_tag_name('svg')
            profile_settings['kid'] = True
        except NoSuchElementException:
            profile_settings['kid'] = False

        current_language = self.driver.find_element(*self.CURRENT_LANGUAGE)
        profile_settings['current_language'] = current_language.text

        maturity_dropdown = self.driver.find_element(*self.MATURITY_DROPDOWN)
        profile_settings['allowed_shows'] = maturity_dropdown.text

        autoplay_episode_checkbox = self.driver.find_element(*self.AUTOPLAY_EPISODES_CHECKBOX)
        # IF THE CHECKBOX IS CHECKED, AN SVG CHILD ELEMENT IS CREATED.
        # THUS CHECKED IFF SVG CHILD EXISTS
        try:
            autoplay_episode_checkbox.find_element_by_tag_name('svg')
            profile_settings['autoplay_episode'] = True
        except NoSuchElementException:
            profile_settings['autoplay_episode'] = False

        autoplay_previews_checkbox = self.driver.find_element(*self.AUTOPLAY_PREVIEWS_CHECKBOX)
        # IF THE CHECKBOX IS CHECKED, AN SVG CHILD ELEMENT IS CREATED.
        # THUS CHECKED IFF SVG CHILD EXISTS
        try:
            autoplay_previews_checkbox.find_element_by_tag_name('svg')
            profile_settings['autoplay_previews'] = True
        except NoSuchElementException:
            profile_settings['autoplay_previews'] = False

        return profile_settings

    def change_profile_settings(self, **kwargs):
        """ CHANGE ONE OF THE FOLLOWING SETTINGS
                name: str
                kid?: bool
                current_language: str
                allowed_shows: str
                autoplay_episode: bool
                autoplay_previews: bool
        """
        """ TODO- "nice to have". a master function that changes multiple settings
        """
        pass

    def change_profile_name(self, new_name: str):
        """ TODO """
        name_field = self.driver.find_element(*self.NAME_INPUT_FIELD)
        name_field.clear()
        name_field.send_keys(new_name)

    def change_kid_bool(self, new_bool: bool):
        """ """
        # clicking the checkbox works for unchecking and checking
        kids_checkbox = self.driver.find_element(*self.CHECKBOX_KIDS)
        kids_checkbox.click()

    def change_default_language(self, new_language: str):
        """ There are 26 languages, most not UTF-8 compliant. TODO- Create and display a dictionary
        soa user of this script could choose a corresponding key to a language, then
        { 'english': 4, 'Español':5, 'Français',:6 } take the value and pass it into nth:child
        """
        if new_language.lower() == 'english':
            language_dropdown = self.driver.find_element(*self.LANGUAGE_DROPDOWN)
            language_dropdown.click()
            english_choice = self.driver.find_element(*self.ENGLISH_CHOICE)
            english_choice.click()
        if new_language.lower() == 'español':
            language_dropdown = self.driver.find_element(*self.LANGUAGE_DROPDOWN)
            language_dropdown.click()
            spanish_choice = self.driver.find_element(*self.SPANISH_CHOICE)
            spanish_choice.click()

    def change_allowed_shows(self, new_allowed_shows):
        """TODO- BUG- in here somewhere. looks good 99% of the time"""
        """ opening and closing the edit modal will be handled elsewhere"""
        current_profile_settings = self.get_profile_settings()
        maturity_dropdown = self.driver.find_element(*self.MATURITY_DROPDOWN)
        maturity_dropdown.click()

        if new_allowed_shows.lower() == 'for little kids only':
            option = 1
        elif new_allowed_shows.lower() == 'for older kids and below':
            option = 2
        elif new_allowed_shows.lower() == 'for teens and below':
            option = 3
            # NETFLI HIDES THE LAST TWO OPTIONS IF kids_checkbox is checked
            if current_profile_settings['kid']:
                self.change_kid_bool(False)
                time.sleep(3)  # TODO-Using time.sleep is laziness. REFACTOR
        elif new_allowed_shows.lower() == 'all maturity levels':
            option = 4
            # NETFLI HIDES THE LAST TWO OPTIONS IF kids_checkbox is checked
            if current_profile_settings['kid']:
                self.change_kid_bool(False)
                time.sleep(3)
        else:
            raise TypeError("DIDNT RECOGNIZED new_allowed_shows param in changed_allowed_shows")

        dropdown_choice = self.driver.find_element_by_css_selector(
            'div[data-uia="maturity-drop-down"] > div.sub-menu.theme-lakira > ul > li:nth-of-type('
            + str(option) + ')'
        )
        dropdown_choice.click()

    def change_autoplay_episode(self, new_bool: bool):
        """ opening and closing the edit modal will be handled elsewhere"""
        autoplay_episode_checkbox = self.driver.find_element(*self.AUTOPLAY_EPISODES_CHECKBOX)
        autoplay_episode_checkbox.click()

    def change_autoplay_previews(self, new_bool: bool):
        """ opening and closing the edit modal will be handled elsewhere"""
        autoplay_previews_checkbox = self.driver.find_element(*self.AUTOPLAY_PREVIEWS_CHECKBOX)
        autoplay_previews_checkbox.click()
