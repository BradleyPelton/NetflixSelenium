from collections import defaultdict
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from login import user_login
import secrets
import mylisttools
import showtools
import genrepagetools

user_login(secrets.bradleys_email,secrets.bradleys_password)

https://www.netflix.com/profiles/manage

#########################################################################
#########################################################################
#########################################################################
# MANAGE PROFILES IS NOT THE SAME THING AS SELECT PROFILE
# WHEN A USER LOGS INTO NETFLIX, THEY ARE ASKED TO SELECT A PROFILE
# DO NOT CONFUSE THE TWO
#########################################################################
#########################################################################
#########################################################################


def get_number_of_profiles(driver) -> int:
    """ Netflix accounts can only have 5 different users.
    """
    profiles = driver.find_elements_by_css_selector('ul.choose-profile > li')
    number_of_profiles = len([profile for profile in profiles if profile.text != "Add Profile"])
    print(number_of_profiles)


def get_profile_names(driver) -> List:
    """ TODO""" 
    profiles = driver.find_elements_by_css_selector('ul.choose-profile > li')
    profile_names = [profile.text for profile in profiles if profile.text != "Add Profile"]
    return(profile_names)

def edit_profile_is_open(driver) -> bool:
    """returns true if the edit profile modal is open, false if else"""
    try:
        driver.find_element_by_css_selector('div.profile-edit-inputs > input')  # name_field 
        return(True)
    except NoSuchElementException:
        return(False)

def open_named_profile(driver, profile_name):
    """ opens the profile with name: profile_name. 
    https://www.netflix.com/ManageProfiles MUST BE OPEN """
    #
    assert driver.current_url == 'https://www.netflix.com/ManageProfiles', 'wrong location'
    profiles = driver.find_elements_by_css_selector('ul.choose-profile > li')
    for profile in profiles:
        if profile.text == profile_name:
            avatar_wrapper = profile.find_element_by_css_selector('div.avatar-wrapper')
            avatar_wrapper.click()
            break


def create_new_profile(driver, profile_name: str, for_kids=False, for_teens=False):
    """ for_kids or for_teens ARE MUTUALLY EXCLUSIVE, CAN'T BE BOTH"""
    """ NEEDS TO BE PERFORMED FROM https://www.netflix.com/ManageProfiles , NOT INITIAL BROWSE"""
    if for_kids and for_teens:
        return("CREATE_NEW_PROFILE TEST IS BOMBING OUT, CANT ACCEPT BOTH FOR_KIDS and FOR_TEENS")
    #
    add_profile_button = driver.find_element_by_css_selector('div.addProfileIcon.icon-tvuiAdd')
    add_profile_button.click()
    # Wait for the new profile creation modal to launch
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, 'input[id="add-profile-name"]')))
    name_field = driver.find_element_by_css_selector('input[id="add-profile-name"]')
    name_field.send_keys(profile_name)
    #
    if for_kids:
        kids_checkbox = driver.find_element_by_css_selector('div.add-kids-option')
        kids_checkbox.click()
    if for_teens:
        teens_checkbox = driver.find_element_by_css_selector('div.add-teen-option')
        teens_checkbox.click()
    #
    continue_button = driver.find_element_by_css_selector(
        'span.profile-button.preferred-action.preferred-active'
    )
    continue_button.click()


def delete_profile(driver, the_profile_name):
    """ TODO- CLEAN THIS UP. FILTHY"""
    """ opening and closing the edit modal will be handled elsewhere"""
    all_profile_names = get_profile_names(driver)
    assert the_profile_name in all_profile_names, "Attempted to delete unknown profile"
    # refactor this, awkward and duplicate logic
    profiles = driver.find_elements_by_css_selector('ul.choose-profile > li')
    for profile in profiles:
        if profile.text == the_profile_name:
            avatar_wrapper = profile.find_element_by_css_selector('div.avatar-wrapper')
            avatar_wrapper.click()
            break
            # wait edit options to appear
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, 'span[data-uia="profile-delete-button"]')))
    delete_button = driver.find_element_by_css_selector(
        'span[data-uia="profile-delete-button"]')
    delete_button.click()
    # wait until deletion_confirmation dialogue appears
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, 'span.profile-button')))
    delete_profile_confirmation_button = driver.find_elements_by_css_selector('span.profile-button')[1]
    delete_profile_confirmation_button.click()


def get_profile_settings(driver) -> dict:
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
    #
    name_field = driver.find_element_by_css_selector('div.profile-edit-inputs > input')
    profile_settings['name'] = name_field.get_attribute('value')
    #
    kids_checkbox = driver.find_element_by_css_selector('label[for="add-kids-profile"]')
    # IF THE CHECKBOX IS CHECKED, AN SVG CHILD ELEMENT IS CREATED. THUS CHECKED IFF SVG CHILD EXISTS
    try:
        kids_checkbox.find_element_by_tag_name('svg')
        profile_settings['kid'] = True
    except NoSuchElementException:
        profile_settings['kid'] = False
    #
    current_language = driver.find_element_by_css_selector('a.user-lang-link').text
    profile_settings['current_language'] = current_language
    #
    maturity_dropdown = driver.find_element_by_css_selector('div[data-uia="maturity-drop-down"]')
    profile_settings['allowed_shows'] = maturity_dropdown.text
    #
    autoplay_episode_checkbox = driver.find_element_by_css_selector(
        'label[for="nextEpisode-profile"]'
    )
    # IF THE CHECKBOX IS CHECKED, AN SVG CHILD ELEMENT IS CREATED. THUS CHECKED IFF SVG CHILD EXISTS
    try:
        autoplay_episode_checkbox.find_element_by_tag_name('svg')
        profile_settings['autoplay_episode'] = True
    except NoSuchElementException:
        profile_settings['autoplay_episode'] = False
    #
    autoplay_previews_checkbox = driver.find_element_by_css_selector(
    'label[for="videomerch-profile"]'
    )
    # IF THE CHECKBOX IS CHECKED, AN SVG CHILD ELEMENT IS CREATED. THUS CHECKED IFF SVG CHILD EXISTS
    try:
        autoplay_previews_checkbox.find_element_by_tag_name('svg')
        profile_settings['autoplay_previews'] = True
    except NoSuchElementException:
        profile_settings['autoplay_previews'] = False
    return(profile_settings)


def change_profile_settings(driver, **kwargs):
    """ CHANGE ONE OF THE FOLLOWING SETTINGS
            name: str
            kid?: bool
            current_language: str
            allowed_shows: str
            autoplay_episode: bool
            autoplay_previews: bool
    """
    """ TODO- "nice to have". a master function that changes all of the settings at the same time
    """
    pass

def change_profile_name(driver, new_name: str):
    """ TODO """
    """ opening and closing the edit modal will be handled elsewhere"""
    current_profile_settings = get_profile_settings(driver)
    assert new_name != current_profile_settings['name'], "Name is the same. change_profile_name"
    name_field = driver.find_element_by_css_selector('div.profile-edit-inputs > input')
    name_field.clear()
    name_field.send_keys(new_name)

def change_kid_bool(driver, new_bool: bool):
    """TODO"""
    """ opening and closing the edit modal will be handled elsewhere"""
    current_profile_settings = get_profile_settings(driver)
    assert new_bool != current_profile_settings['kid'], 'same kid status, change_kid_bool'
    # clicking the checkbox works for unchecking and checking
    kids_checkbox = driver.find_element_by_css_selector('label[for="add-kids-profile"]')
    kids_checkbox.click()

def change_default_language(driver, new_language: str):
    """ There are 26 languages, most not UTF-8 compliant. TODO- Create and display a dictionary so
    a user of this script could choose a corresponding key to a language, then 
    { 'english': 4, 'Español':5, 'Français',:6 } take the value and pass it into nth:child
    """
    """ opening and closing the edit modal will be handled elsewhere"""
    current_profile_settings = get_profile_settings(driver)
    assert new_language != current_profile_settings['language'], "same language, change_default_lan"
    if new_language.lower() == 'english':
        language_dropdown = driver.find_element_by_css_selector('div.nfDropDown.theme-lakira > div')
        language_dropdown.click()
        english_choice = driver.find_element_by_css_selector(
            'div.sub-menu.theme-lakira > ul > li:nth-of-type(4)'
        )
    if new_language.lower() == 'español':
        language_dropdown = driver.find_element_by_css_selector('div.nfDropDown.theme-lakira > div')
        language_dropdown.click()
        spanish_choice = driver.find_element_by_css_selector(
        'div.sub-menu.theme-lakira > ul > li:nth-of-type(5)'
        )
        spanish_choice.click()

def change_allowed_shows(driver, new_allowed_shows):
    """TODO- BUG- in here somewhere. looks good 99% of the time"""
    """ opening and closing the edit modal will be handled elsewhere"""
    current_profile_settings = get_profile_settings(driver)
    assert new_allowed_shows != current_profile_settings['allowed_shows']
    maturity_dropdown = driver.find_element_by_css_selector('div[data-uia="maturity-drop-down"]')
    maturity_dropdown.click()
    # print('gate 1')
    #
    if new_allowed_shows.lower() == 'for little kids only':
        option = 1
    #
    elif new_allowed_shows.lower() == 'for older kids and below':
        option = 2
    elif new_allowed_shows.lower() == 'for teens and below':
        option = 3
        # NETFLI HIDES THE LAST TWO OPTIONS IF kids_checkbox is checked
        if current_profile_settings['kid']:
            change_kid_bool(driver,False)
            time.sleep(3)
    elif new_allowed_shows.lower() == 'all maturity levels':
        option = 4
        # NETFLI HIDES THE LAST TWO OPTIONS IF kids_checkbox is checked
        if current_profile_settings['kid']:
            change_kid_bool(driver,False)
            time.sleep(3)
    else:
        raise TypeError("DIDNT RECOGNIZED new_allowed_shows parameter in changed_allowed_shows")
    #
    # print('gate 2')
    dropdown_choice = driver.find_element_by_css_selector(
        'div[data-uia="maturity-drop-down"] > div.sub-menu.theme-lakira > ul > li:nth-of-type(' \
        + str(option) + ')'
    )
    dropdown_choice.click()

# change_allowed_shows(driver, 'for teens and below')
# change_allowed_shows(driver, 'all maturity levels')
# change_allowed_shows(driver, 'for older kids and below')
# change_allowed_shows(driver, 'for little kids only')

def change_autoplay_episode(driver, new_bool: bool):
    """ opening and closing the edit modal will be handled elsewhere"""
    current_profile_settings = get_profile_settings(driver)
    assert new_bool != current_profile_settings['autoplay_episode'], "same bool, change_autoplay_e"
    autoplay_episode_checkbox = driver.find_element_by_css_selector(
        'label[for="nextEpisode-profile"]'
    )
    autoplay_episode_checkbox.click()


def change_autoplay_previews(driver, new_bool: bool):
    """ opening and closing the edit modal will be handled elsewhere"""
    current_profile_settings = get_profile_settings(driver)
    assert new_bool != current_profile_settings['autoplay_previews'], "same bool, change_autoplay_p"
    #
    autoplay_previews_checkbox = driver.find_element_by_css_selector(
    'label[for="videomerch-profile"]'
    )
    autoplay_previews_checkbox.click()