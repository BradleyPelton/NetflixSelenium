from typing import List, Dict
from collections import defaultdict

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from login import user_login
import secrets
import mylisttools
import showtools

# MOVIES AND SHOWS HAVE HIDDEN GENRES AND PUBLIC GENRES
# A PUBLIC GENRE IS SOMETHING LIKE "ROMANCE", "ACTION", "HORROR"
# A HIDDEN GENRE IS ASSIGNED BY NETFLIX AND DISPLAYED IN THE U
# E.G https://www.netflix.com/browse/genre/83 FOR "Tv Shows"

# TODO- There are three other sort methods: Suggested for you, Z-A, Year Released
# CREATE FUCNTIONS FOR EACH OF THESE
#


def switch_to_grid(driver):
    """
    switch from the default row display( that scroll right to display more)
    to the grid view pattern
    by clicking the grid pattern button
    """
    switch_to_grid_view_button = driver.find_element_by_css_selector('button.aro-grid-toggle')
    switch_to_grid_view_button.click()


def switch_to_alpha_sort(driver):
    """
    click the dropdown that allows user to change the sort method
    change the sort method to alpha
    """
    dropdown_sort = driver.find_element_by_css_selector('div.nfDropDown.widthRestricted.theme-aro')
    dropdown_sort.click()

    a_through_z_sort_option = driver.find_element_by_css_selector('div.sub-menu.theme-aro > ul > li:nth-child(3)')
    a_through_z_sort_option.click()

# current_sort_option = driver.find_element_by_css_selector('div.nfDropDown.widthRestricted.theme-aro > div')
# print(f"Currently sourting by {current_sort_option.text}")


def master_sweep(driver, genre_id: int) -> dict:
    """ MASTER SWEEP  TODO- GENERALIZE, STILL USES ANIME NAMES"""
    driver.get("https://www.netflix.com/browse/genre/" + str(genre_id))
    switch_to_grid(driver)

    shows = driver.find_elements_by_css_selector('a[class="slider-refocus"]')

    anime_shows_dict = defaultdict(dict)
    for show in shows[0:10]:
        title = show.text
        anime_shows_dict[title] = {}  #add show title to 
        # OPEN JAWBONE
        show.click()
        # Let jawbone load, explicit wait until jawbone is open
        wait = WebDriverWait(driver,10)
        meta_lists_element = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'div.meta-lists')))
        #
        if showtools.show_has_saved_progress(driver, show, JAWBONE_OPEN=True):
            anime_shows_dict[title]['progress'] = 'T'
        else:
            anime_shows_dict[title]['progress'] = 'F'
        #
        if mylisttools.is_in_my_list(driver, show, JAWBONE_OPEN=True):
            anime_shows_dict[title]['is_in_my_list'] = 'T'
        else:
            anime_shows_dict[title]['is_in_my_list'] = 'F'
        #
        anime_shows_dict[title]['actors'] = showtools.get_actors_list(driver, show, JAWBONE_OPEN=True)
        anime_shows_dict[title]['genres'] = showtools.get_genre_list(driver, show, JAWBONE_OPEN=True)
        anime_shows_dict[title]['tags'] = showtools.get_tags_list(driver, show, JAWBONE_OPEN=True)
        #
        jawBone_close_button = driver.find_element_by_css_selector('button.close-button.icon-close')
        jawBone_close_button.click()
        #
        # explicitly waiting until jawbone is closed
        closed_jawbone = wait.until(EC.invisibility_of_element_located(jawBone_close_button))



