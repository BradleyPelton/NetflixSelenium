import time
from collections import defaultdict

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


from login import driver, user_login
import secrets
import mylisttools
import showtools
import genrepagetools

# the homepage of netflix is netflix.com/browse
# After successful login, users are redirected to `netflix.com/browse`
# netflix.com is redirected to this home page as well `netflix.com/browse`

driver.get('https://netflix.com')


def get_main_recommendation_id(driver) -> int:
    """returns the id for the show that is the primary "ad" seen on the top
    of the home page. The first thing a user sees. Usually 4/5ths of the screen
    NETFLIX CALLS THIS THE MAIN BILLBOARD
    """
    # the main page doesnt display almost any of the information displayed
    # in the JAWBONE. I would rather not redirect to /title/80050063 to retrieve
    # all of this information, but it might be unavoidable
    # TODO- RETURN MORE INFORMATION THAN JUST THE ID

    more_info_button = driver.find_element_by_css_selector(
        'a[data-uia="play-button"] + a')
    # sibling to the play button. TODO- Maybe cleaner css?
    title_link = more_info_button.get_attribute('href')
    title_id = int(title_link.split("/")[-1])
    return(title_id)


def play_main_recommendation(driver):
    """play the giant billboard ad from /browse """
    billboard_play = driver.find_element_by_css_selector(
        'div.billboard-row  a.playLink'
    )
    # This looks like sloppy css, but the main issue here is that there is an near-identical
    # Billboard ad about half way down the page. This other billboard ad has about same button
    # layout. The only way to guarantee uniqueness of the play button is to approach way up the
    # dom
    billboard_play.click()


def get_shows_in_continue_watching(driver) -> list:
    """ returns a list of shows that are displayed in 'Continue Watching for Bradley' row """
    """TODO TODO TODO"""
    pass


def get_recommended_genres(driver) -> list:
    """ TODO- BREAK THIS INTO MULTIPLE FUNCTIONS:
    NAMELY: TOP 10 US, TOP PICKS FOR BRADLEY, GENRES(THIS FUNCTION), ETC.
    """
    # ASSUMES DRIVER IS ALREADY AT THE HOME PAGE

    # SCROLL TO THE BUTTOM OF THE HOME PAGE
    # 10 lazy loads by netflix. Have to scroll to the bottom, then more loads
    # repeat 10 times
    for i in range(10):
        driver.execute_script("window.scrollTo(0, 10000000)")
        print(i)
        time.sleep(1)

    # THIS IS GENRES AND "My List"
    genre_rows = driver.find_elements_by_css_selector('a.rowTitle')
    genres = [genre.text for genre in genre_rows]
    return(genres)
    # for row in rows:
    #     print(row.text)
    # #notably includes:
    # My List
    # Because you watched Cells at Work!
    # New Releases
    # #notably excludes:
    # Continue Watching for Bradley
    # Popular on netflix
    # Trending Now
    # Top 10 in the U.s. Today
    # Top Picks for Bradley
    # Because you added Goodfellas to your List

    # # this was an interesting idea, but the element that contains the title
    # # is the sibling before the id=row-37 element. We cant go backwards or up with css
    # for i in range(0,38):
    #     row = driver.find_element_by_css_selector('#row-'+str(i))

###########################################################################################
###########################################################################################
###########################################################################################
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= HEADER FUNCTIONS =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#  THE FOLLOWING FUNCTIONS ARE NOT SPECIFIC TO THE HOMEPAGE. ALL PAGES HAVE ACCESS TO THIS HEADER
# AND THUS ALL OF THESE FUNCIONS. TODO- DECIDE WHETHER THESE FUNCIONS SHOULD HAVE THEIR OWN PAGE
###########################################################################################
###########################################################################################
###########################################################################################


def logout(driver):
    """ self explantory, tested"""
    account_dropdown_button = driver.find_element_by_css_selector('div.account-dropdown-button')
    account_dropdown_button.click()
    # time.sleep(3)
    dropdown_options = driver.find_elements_by_css_selector('ul.account-links.sub-menu-list > li')

    logout_button = dropdown_options[2]
    logout_button.click()


def navigate_to_manage_profile(driver):
    """ navigate to the manage profiles page, https://www.netflix.com/profiles/manage, by clicking
    on the manage profiles button from the account dropdown from the header
    """
    """ NOTE- while these functions contribute to completeness by testing individual buttons, it
    is much more important to test key features in the first version of the automation suite"""
    account_dropdown_button = driver.find_element_by_css_selector('div.account-dropdown-button')
    account_dropdown_button.click()
    #
    manage_profiles_button = driver.find_element_by_css_selector('a[aria-label="Manage Profiles"]')
    manage_profiles_button.click()


def clear_notifications(driver):
    """ CLEAR NOTIFICATIONS BY OPENING THE NOTIFICATIONS DROPDOWN AND THEN CLOSING IT"""
    """ TODO- NEED NOTIFIATIONS TO APPEAR AGAIN TO TEST. TODO"""
    notifications_menu_button = driver.find_element_by_css_selector(
        'button[aria-label="Notifications"]'
    )
    notifications_menu_button.click()
    notifications_menu_button.click()


def click_top_notification(driver):
    """ self-explanatory. Works from every non-video page"""
    notifications_menu_button = driver.find_element_by_css_selector(
        'button[aria-label="Notifications"]'
    )
    notifications_menu_button.click()
    #
    notifications_container = driver.find_element_by_css_selector('ul.notifications-container')
    notifications = notifications_container.find_elements_by_css_selector('div > li.notification')
    #
    top_notification = notifications[0]
    top_notification.click()


def search_field_is_open(driver) -> bool:
    """ return True if the search field is open, False if else"""
    try:
        driver.find_element_by_css_selector('input[data-uia="search-box-input"]')
        return(True)
    except NoSuchElementException:
        return(False)


def clear_search(driver):
    """ search field is non-empty IFF it is open. Thus we dont have to open the search field
     here"""
    search_field = driver.find_element_by_css_selector('input[data-uia="search-box-input"]')
    search_field.clear()


def search(driver, search_term: str):
    """ uses the search bar in the header to search for search_term"""
    """ TODO- This is a exactly what a serach is in theory, but in practice, Netflix handles things
    a little differently. Notice when searching things manually, the netflix app actually searches
    after EVERY SINGLE key press. Thus if we were to search for "Top Gun" manually, the observer
    will notice that 7 DIFFERENT page results are displayed in the results (len("Top Gun")). This
    is the fundamental difference between automation testing and automating user behavior. We need
    to actually mimic user behavior. In this case the 2 differ because Selenium.send_keys() sends
    all of the keys at the same time. TODO- THIS IS GOOD THEORY. GOOD DISCUSSION. READDD MEEEE"""
    if search_field_is_open(driver):
        clear_search(driver)
    else:
        # TODO- Turn open_seach_field into a function??? Seems a little verbose
        search_button = driver.find_element_by_css_selector('button.searchTab')
        search_button.click()
    search_field = driver.find_element_by_css_selector('input[data-uia="search-box-input"]')
    search_field.send_keys(search_term)


# def click_refer_button(driver):
#     """ waste of time. adding it here just for completeness"""
#     pass
