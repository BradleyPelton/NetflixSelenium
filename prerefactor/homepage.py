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

#################################################################################################
# ROW OPERATIONS
# The following funcitions are going to frequently use the following element:
# row = div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card
# ALL HOMEPAGE ROWS ARE LOCATED IN CONTAINERS LIKE THIS
# ROW_ELEMENT, ROW,  WILL ONLY REFERENCE THESE CONTAINERS AND ROWS SHOULD BE CONSIDERED THIS
#################################################################################################
 

def get_shows_in_continue_watching(driver) -> list:
    """ returns a list of shows that are displayed in 'Continue Watching for Bradley' row """
    """TODO TODO TODO"""
    pass


# def get_all_rows(driver) -> list:
"""TODO- NOT FUCNTIONAL. SOME ROWS ARE NOT ROWS BUT BILLBOARDS/TOP 10 lists ETC"""
#     """ return a list of Webelements that represent the rows of the home page"""
#     row_container = driver.find_element_by_css_selector('div.lolomo.is-fullbleed')
#     rows = row_container.find_elements_by_css_selector('div.lolomoRow.lolomoRow_title_card')
a = driver.find_elements_by_css_selector(
    'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card[data-list-context]')
# len(a)
# ORDER OF ROWS. I WONDER IF THIS IS UNIVERSAL OR USER SPECIFIC. 
# ['queue', 'continueWatching', 'becauseYouAdded', 'trendingNow', 'bigRow', 'genre', 'genre', 'popularTitles', 'genre', 'genre', 'similars', 'genre', 'mostWatched', 'genre', 'netflixOriginals', 'genre', 'similars', 'genre', 'topTen', 'genre', 'genre', 'genre', 'genre', 'genre', 'genre', 'genre', 'genre', 'genre', 'newRelease', 'genre', 'genre', 'similars', 'genre', 'similars', 'genre', 'genre', 'similars', 'genre', 'becauseYouAdded', 'similars']

#UNIQUE ROWS
# ['popularTitles', 'newRelease', 'netflixOriginals', 'continueWatching', 'topTen', 'queue', 'trendingNow', 'mostWatched', 'similars', 'genre', 'bigRow', 'becauseYouAdded']


def get_genre_rows(driver) -> list:
    """get all genre rows that are not targeted at me e.g. Action movies but not 'Because you.. """
    genre_rows = driver.find_elements_by_css_selector(
        'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card[data-list-context="genre"]')
    return(genre_rows)


def get_queue_row(driver):
    """ queue row AKA My-List row"""
    queue_row = driver.find_element_by_css_selector(
        'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card[data-list-context="queue"]'
    )
    return(queue_row)


def get_continueWatching_row(driver):
    """ continueWatching row is the shows that currently have saved progress """
    continueWatching_row = driver.find_elements_by_css_selector(
        'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card[data-list-context="continueWatching"]')
    return(continueWatching_row)


def get_trendingNow_row(driver):
    """row? rows? TODO """
    trendingNow = driver.find_elements_by_css_selector(
        'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card[data-list-context="trendingNow"]')
    return(trendingNow)


def get_similars_rows(driver) -> list:
    """rows with data-list-context="similars" . These are rows that are targeted at the profile"""
    similars_rows = driver.find_elements_by_css_selector(
        'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card[data-list-context="similars"]')
    return(similars_rows)


def get_becauseYouAdded_rows(driver) -> list:
    """ BUG- see get_row_titles_from_row_list"""
    """rows with data-list-context="becauseYouAdded". These rows are targetd at the profile based
    on the user having added the show the row is named after (e.g. Because you Added Top Gun)
    """
    becauseYouAdded_rows = driver.find_elements_by_css_selector(
        'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card[data-list-context="becauseYouAdded"]')
    return(becauseYouAdded_rows)


def get_newRelease_rows(driver) -> list:
    """ TODO"""
    newRelease_rows = driver.find_elements_by_css_selector(
        'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card[data-list-context="newRelease"]')
    return(newRelease_rows)


def get_topTen_rows(driver) -> list:
    """ row? rows? TODO find out"""
    """ TODO"""
    topTen_rows = driver.find_elements_by_css_selector(
        'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card[data-list-context="topTen"]')
    return(topTen_rows)


def get_netflixOriginals_rows(driver) -> list:
    """ row? rows? TODO find out"""
    """ TODO"""
    netflixOriginals_rows = driver.find_elements_by_css_selector(
        'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card[data-list-context="netflixOriginals"]')
    return(netflixOriginals_rows)


def get_popularTitles_rows(driver) -> list:
    """ row? rows? TODO find out"""
    """ TODO"""
    popularTitles_rows = driver.find_elements_by_css_selector(
        'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card[data-list-context="popularTitles"]')
    return(popularTitles_rows)


def get_bigRow_rows(driver) -> list:
    """ row? rows? TODO find out"""
    """ TODO"""
    bigRow_rows = driver.find_elements_by_css_selector(
        'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card[data-list-context="bigRow"]')
    return(bigRow_rows)


def get_mostWatched_rows(driver) -> list:
    """ row? rows? TODO find out"""
    """ TODO"""
    mostWatched_rows = driver.find_elements_by_css_selector(
        'div.lolomo.is-fullbleed > div.lolomoRow.lolomoRow_title_card[data-list-context="mostWatched"]')
    return(mostWatched_rows)


def get_row_titles_from_row_list(driver, row_list: list) -> list:
    """ INPUT: list of WEBELEMENTS of row elements (div.lolomoRow.lolomoRow_title_card)
        OUTPUT: THE LIST OF TITLES FOR THOSE ROW ELEMENTS
    """
    # BUG- TODO- for some reason, get_becauseYouAdded_rows have the title stored in a span.rowTitle
    # instead of a.rowTitle.  FIX BUG TODO Investigate other rows
    row_title_list = []
    for row in row_list:
        row_title = row.find_element_by_css_selector('a.rowTitle')
        # print(row_title.text)
        row_title_list.append(row_title.text)
    return(row_title_list)


def row_page_right(driver, row_element):
    """take in the row_element and click the chevron right to see the next page of shows"""
    right_chevron = row_element.find_element_by_css_selector('span.handle.handleNext.active')
    right_chevron.click()
    # BUG- SOMETIMES I CANT PAGE RIGHT. ElementClickInterceptedException


def row_page_left(driver, row_element):
    """take in the row_element and click the chevron left to see the previous page of shows. LEFT
    DOESNT EXIST FOR SOME ROWS UNTIL RIGHT IS CLICKED ONCE (and thus there is something to go left)
    """
    left_chevron = row_element.find_element_by_css_selector('span.handle.handlePrev.active')
    left_chevron.click()


def get_recommended_genres(driver) -> list:
    """TODO """
    # SCROLL TO THE BUTTOM OF THE HOME PAGE
    # 10 lazy loads by netflix. Have to scroll to the bottom, then more loads
    # repeat 10 times
    for i in range(10):
        driver.execute_script("window.scrollTo(0, 10000000)")
        print(i)
        time.sleep(1)
    #
    genre_rows = get_genre_rows(driver)
    genres = [genre.text for genre in genre_rows]
    return(genres)

# NOTE TO READER. ANY FUNCTIONS RELATED TO INTERACTING WITH SHOW ELEMNTS CAN BE FOUND IN 
# showtools.py. THE FOLLOWING FUCNTIONS ARE SQUARELY IN THE DOMAIN OF ROW_ELEMENT FUCNTIONS
def get_show_titles_from_row(driver, row_element):
    """ this one is complicated. Netflix's frontend doesnt populate the DOM with all of the shows.
    the test suite needs to force all of the shows to load by using get_page_right()
    Even worse yet, the last row is populated with the elements of the first row if the last row
    doent fill the entire row. EEEEVEEEENNNNN WORSE YET, the number of shows displayed varies on
    the size of the screen. TODO- SLOW AND HIDEOUS, BUT FUNCTIONAL
    """
    # Note from/to author: This is not a data scraping job. This is a test suite
    final_show_titles_list = []
    for _ in range(20):
        currently_displayed_shows = row_element.find_elements_by_css_selector('a[class="slider-refocus"]')
        current_titles = [
            show.text 
            for show in currently_displayed_shows
            if show.text not in final_show_titles_list
            and show.text != ''
        ]
        if not current_titles:
            break
        else:
            final_show_titles_list += current_titles
            # print(current_titles)
            # print(final_show_titles_list)
            row_page_right(driver,row_element)
            time.sleep(1)
    return(final_show_titles_list)


def get_first_show_in_row(driver, row_element):
    """ return a show_element. NOTE- SHOW ELEMENTS ARE JUST AS SPECIAL AS ROW_ELEMNTS. THIS
    TEST SUITE CONSIDERS THE TWO TO BE FUNDAMENTAL. THUS THE SHOW_ELEMENT MUST FIT THE STANDARDS
    , i.e. show = driver.find_elements_by_css_selector('a[class="slider-refocus"]') """
    # TODO- NOTE- TODO
    pass

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
