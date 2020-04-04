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

# https://www.netflix.com/profiles/manage

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
    """ PROFILE HAS TO BE OPEN TODO- WRITE A FUCNTION THAT OPENS THIS PAGE"""
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
    print(profile_settings)


def change_profile_settings(
    driver,
    name=False,
    kid=False,
    current_language=False,
    allowed_shows=False,
    autoplay_episode=False,
    autoplay_previews=False
)
    """ CHANGE ONE OF THE FOLLOWING SETTINGS
            name: str
            kid?: bool
            current_language: str
            allowed_shows: str
            autoplay_episode: bool
            autoplay_previews: bool
    """