from typing import List, Dict
from collections import defaultdict

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from login import driver, user_login
import secrets
import mylisttools
import showtools



def show_has_saved_progress(driver, show_element, JAWBONE_OPEN=False) -> bool:
    """ CHECK IF SHOW HAS SAVED PROGRESS, if so return False, else False"""
    open_jawbone_if_not_open(driver, show_element, JAWBONE_OPEN)
    try:
        progress_summary = driver.find_element_by_css_selector('span.summary')
        print(f"show {show_element.text} has saved progress. {progress_summary.text} remain")
        return(True)
    except NoSuchElementException:
        return(False)


def has_new_episodes(driver, show_element, JAWBONE_OPEN=False) -> bool:
    """ IF A SHOW HAS the "NEW EPISODES" tile added to the image, return True
    false if else"""
    # 
    pass


def is_netflix_original(driver, show_element, JAWBONE_OPEN=False) -> bool:
    """ return true if netflix original, false if else"""
    # this one might be tricky. The only designation that a show is a Netflix
    # original seems to be the "N SERIES" logo that is added on to the series
    # logo(same image). Might have to compare against a list of confirmed
    # netflix originals or do some cool image analysis to see if the top left
    # pixel is the nextflix red
    pass


def get_maturity_rating(driver, show_element, JAWBONE_OPEN=False) -> str:
    """ return the maturity rating for a show, E.G. 'PG', 'PG-13', 'TV-MA'"""
    """ UNTESTED, TODO- TEST"""
    rating = driver.find_element_by_css_selector('span.maturity-rating > span.maturity-number')
    return(rating.text)


def get_show_match_percentage(driver, show_element, JAWBONE_OPEN=False) -> int:
    """ returns the match percentage e.g. '99% Match' for Castlevania"""
    """ EDGE CASE: match percentage doesnt seem to always show"""
    pass

def get_release_date():
    """UNTESTED TODO-TEST"""
    year = driver.find_element_by_css_selector('span.year')
    return(year.text)

def get_number_of_seasons_and_episodes():
    pass


def get_actors_list(driver, show_element, JAWBONE_OPEN=False) -> List:
    """ returns list of actors. TODO- IF actors arent available from JAWBONE,
    write the logic to navigate to the details tab of the jawbone, scrape the 
    top 3 actors, and then return that.
    """
    open_jawbone_if_not_open(driver, show_element, JAWBONE_OPEN)
    try:
        # not sure why I cant just add " > a" to the end of the css selector for cast _element
        # 
        cast_element_list = driver.find_element_by_css_selector('div.meta-lists > p.cast.inline-list')
        actors_elements = cast_element_list.find_elements_by_tag_name('a')
        actors = [element.text for element in actors_elements]
        return(actors)
    except NoSuchElementException:
        return(["COULD NOT FIND ACTORS"])


def get_genre_list(driver, show_element, JAWBONE_OPEN=False) -> List:
    """ return a genre list if available. TODO- if not avaiable, scrape details"""
    open_jawbone_if_not_open(driver, show_element, JAWBONE_OPEN)
    try:
        genre_element_list = driver.find_element_by_css_selector('div.meta-lists > p.genres.inline-list')
        genres_a_tags = genre_element_list.find_elements_by_tag_name('a')
        genres = [element.text for element in genres_a_tags]
        return(genres)
    except NoSuchElementException:
        return(["COULD NOT FIND GENRES"])


def get_tags_list(driver, show_element, JAWBONE_OPEN=False) -> List:
    """ return a tags list if available. TODO- if not avaiable, scrape details"""
    open_jawbone_if_not_open(driver, show_element, JAWBONE_OPEN)
    try:
        tags_element_list = driver.find_element_by_css_selector('div.meta-lists > p.tags.inline-list')
        tags_a_elements = tags_element_list.find_elements_by_tag_name('a')
        tags = [element.text for element in tags_a_elements]
        return(tags)
    except NoSuchElementException:
        return(["COULD NOT FIND TAG"])



def is_upvoted(driver, show_element, JAWBONE_OPEN=False):
    """ return bool if upvoted"""
    open_jawbone_if_not_open(driver, show_element, JAWBONE_OPEN)
    try:
        already_upvoted_big_upvote_button = driver.find_element_by_css_selector(
            'a[aria-label="Already rated: thumbs up (click to remove rating)"]')
        return(True)
    except NoSuchElementException:
        return(False)


def is_downvoted(driver, show_element, JAWBONE_OPEN=False):
    """ return bool if upvoted"""
    open_jawbone_if_not_open(driver, show_element, JAWBONE_OPEN)
    try:
        already_downvoted_big_downvoted_button = driver.find_element_by_css_selector(
            'a[aria-label="Already rated: thumbs down (click to remove rating)"]')
        return(True)
    except NoSuchElementException:
        return(False)


def upvote_show(driver, show_element, JAWBONE_OPEN=False):
    """upvote if not already upvoted, pass if already upvoted
        weird edge cases: the upvote button disappears when a show is downvoted"""
    open_jawbone_if_not_open(driver, show_element, JAWBONE_OPEN)
    if is_upvoted(driver, show_element, JAWBONE_OPEN=True):
        print("already upvoted, upvote_show is not doing anything")
    elif is_downvoted(driver, show_element, JAWBONE_OPEN=True):
        already_downvoted_big_downvoted_button = driver.find_element_by_css_selector(
            'a[aria-label="Already rated: thumbs down (click to remove rating)"]')
        already_downvoted_big_downvoted_button.click()
        upvote_button = driver.find_element_by_css_selector('a[aria-label="Rate thumbs up"]')
        upvote_button.click()
    else:
        upvote_button = driver.find_element_by_css_selector('a[aria-label="Rate thumbs up"]')
        upvote_button.click()



def downvote_show(driver, show_element, JAWBONE_OPEN=False):
    """weird edge cases: the upvote button disappears when a show is downvoted"""
    open_jawbone_if_not_open(driver, show_element, JAWBONE_OPEN)
    if is_downvoted(driver, show_element, JAWBONE_OPEN=True):
        print("already downvoted, downvote_show is not doing anything")
    elif is_upvoted(driver, show_element, JAWBONE_OPEN=True):
        already_upvoted_big_upvote_button = driver.find_element_by_css_selector(
            'a[aria-label="Already rated: thumbs up (click to remove rating)"]')
        already_upvoted_big_upvote_button.click()
        downvote_button = driver.find_element_by_css_selector('a[aria-label="Rate thumbs down"]')
        downvote_button.click()
    else:
        downvote_button = driver.find_element_by_css_selector('a[aria-label="Rate thumbs down"]')
        downvote_button.click()


def open_jawbone_if_not_open(driver, show_element, JAWBONE_OPEN):
    if not JAWBONE_OPEN:
        show_element.click()
        wait = WebDriverWait(driver,10)
        meta_lists_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.meta-lists')))
