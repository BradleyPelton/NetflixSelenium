import time
from collections import defaultdict

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


from login import  user_login
import secrets
import mylisttools
import showtools
import genrepagetools

user_login(secrets.bradleys_email,secrets.bradleys_password)

### NOTE- CTRL +K CTRL + 0 TO FOLD ALL, CTRL + K CTRL J TO UNFOLD ALL 



#########################################################################
#########################################################################
#########################################################################
"""TODO- ORGANIZE THESE FUNCTIONS BASED ON THE ORDER THE ELEMENTS APPEAR IN THE JAWBONE"""
#########################################################################
#########################################################################
#########################################################################

# NOTE- SHOW ELEMENTS ARE OFTEN RETURNED FROM ROW_OPERATIONS. SEE homepage.py IF YOU NEED TO 
# GRAB A SHOW ELEMENT FROM A PAGE SINCE EVERY SHOW ELEMENT APPEARS IN A ROW

##### JAWBONE FUCNTIONS
#### FOR SHOW PREVIEW FUNCTIONS, SEE LINE 300+
def play_show(driver, show_element, JAWBONE_OPEN=False):
    """ Plays the show passed in as the parameter show_element """
    """ NOT TESTED, TODO- TEST """
    open_jawbone_if_not_open(driver, show_element, JAWBONE_OPEN)
    
    play_button = driver.find_element_by_css_selector('a[data-uia="play-button"] > span')
    play_button.click()


def is_show(driver, show_element, JAWBONE_OPEN=False):
    """ not sure about needed this function or not. Leaving it here just in case"""
    pass


def is_movie(driver, show_element, JAWBONE_OPEN=False) -> str:
    """ movie is defined as not TV show. Everything is either a series episodes or a movie"""   
    pass


def get_duration(driver, show_element, JAWBONE_OPEN=False) -> str:
    """ RETURNS STR, e.g.'1h 27m' FOR MOVIE, '1 Season' FOR SHOW """
    """ NOT TESTED- TODO- THIS SHOULD RECIEVE EXTRA ATTENTION TO TEST"""
    open_jawbone_if_not_open(driver, show_element, JAWBONE_OPEN)

    duration = driver.find_element_by_css_selector('span.duration')
    return(duration.text)


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
    # Might be equally as hard to determine as _is_netflix_original
    # Netflix adds a "new episodes" box ontop of the the boxart
    # My only idea for runny this function is to improt some module
    # that can determine which pixels are supposed to be the netflix red
    pass


def is_netflix_original(driver, show_element, JAWBONE_OPEN=False) -> bool:
    """ return true if netflix original, false if else"""
    # this one might be tricky. The only designation that a show is a Netflix
    # original seems to be the "N SERIES" logo that is added on to the series
    # logo(same image). Might have to compare against a list of confirmed
    # netflix originals or do some cool image analysis to see if the top left
    # pixel is the nextflix red
    pass


def has_audio_description_available(driver, show_element, JAWBONE_OPEN=False) -> bool:
    """ return True if the show has an audio description available, False if else"""
    open_jawbone_if_not_open(driver, show_element, JAWBONE_OPEN)

    try:
        # used used web element that is found
        audio_description_badge = driver.find_element_by_css_selector(
            'span.audio-description-badge')
        return(True)
    except NoSuchElementException:
        return(False)


def get_maturity_rating(driver, show_element, JAWBONE_OPEN=False) -> str:
    """ return the maturity rating for a show, E.G. 'PG', 'PG-13', 'TV-MA'"""
    """ UNTESTED, TODO- TEST"""
    open_jawbone_if_not_open(driver, show_element, JAWBONE_OPEN)

    rating = driver.find_element_by_css_selector('span.maturity-rating > span.maturity-number')
    return(rating.text)


def get_show_match_percentage(driver, show_element, JAWBONE_OPEN=False) -> str:
    """ returns the match percentage e.g. '99% Match' for Castlevania"""
    """ EDGE CASE: match percentage doesnt seem to always show"""
    """ NOT TESTED, TODO- TEST"""
    open_jawbone_if_not_open(driver, show_element, JAWBONE_OPEN)

    match_score = driver.find_element_by_css_selector('span.match-score')
    # if no match score is displayed, driver will still find the match_score element,
    # but it will just return '' when match_score.text is called. 
    if match_score.text == '':
        return("No match score displayed")
    else:
        return(match_score.text)


def get_synopsis(driver, show_element, JAWBONE_OPEN=False) -> str:
    """NOT TESTED, TODO- TEST"""
    open_jawbone_if_not_open(driver, show_element, JAWBONE_OPEN)

    synopsis = driver.find_element_by_css_selector('div.synopsis')
    return(synopsis.text)


def get_release_date(driver, show_element, JAWBONE_OPEN=False):
    """UNTESTED TODO-TEST"""
    open_jawbone_if_not_open(driver, show_element, JAWBONE_OPEN)

    year = driver.find_element_by_css_selector('span.year')
    return(year.text)


def get_number_of_episodes():
    """not sure if this is going to be hard or not. """
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
        # WAIT UNTIL JAWBONE FINISHES LOADING
        wait = WebDriverWait(driver,10)
        meta_lists_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.meta-lists')))


#################################################################################################
#################################################################################################
#################################################################################################
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- SHOW PREVIEW =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#################################################################################################
#################################################################################################
#################################################################################################

# NOT TO BE CONFUSED WITH THE JAWBONE FUCNTINOS ABOVE, THESE FUCNTIONS SOLELY WORK WITH THE USE 
# CASES WHEN A USER MOUSES OVER A SHOW ELEMENT 

# NETFLIX CALLS THIS THE "BOB-CARD" "BOB OVERLAY" "BOB-JAW-HITZONE"

# Every show hasa bob-container div but it contains nothing until the show is moused over

shows = driver.find_elements_by_css_selector('a[class="slider-refocus"]')
s = shows[25]
mouse_over_show_element(driver, s)
show_is_in_my_list_from_show_preview(driver, s)


def mouse_over_show_element(driver, show_element):
    """ """
    action = ActionChains(driver)
    action.move_to_element(show_element).perform()
    # Wait for BOB CONTAINER to open
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.bob-play-hitzone')))


def mouse_over_show_if_not_moused_over(driver, show_element):
    """ self-explanatory"""
    if show_is_being_previewed(driver):
        pass
    else:
        mouse_over_show_element(driver, show_element)


def show_is_being_previewed(driver):
    """ RETURN TRUE IF THERE IS A SHOW THAT IS CURRENTLY BEING MOUSED OVER. NOT TO BE CONFUSED
    WITH JAWBONE OPEN. STIPULATES THE BOB CONTAINER IS OPEN, SEE showtools.py"""
    """NOTE- only one show can be previewed at a time so its valid just to search the entire dom"""
    try:
        driver.find_element_by_css_selector('div.bob-overview a[data-uia="play-button"]')
        return(True)
    except NoSuchElementException:
        return(False)


def open_jawbone_from_show_preview(driver, show_element):
    """ TODO- add logic to check if jawbone is already open."""
    mouse_over_show_if_not_moused_over(driver, show_element)
    #
    bob_jawbone_hitzone = driver.find_element_by_css_selector(
        'div.bob-overlay > a.bob-jaw-hitzone'
    )
    bob_jawbone_hitzone.click()


def play_show_from_show_preview(driver, show_element):
    """ play the show from the bob container by clicking in the center of the bob container"""
    mouse_over_show_if_not_moused_over(driver, show_element)
    #
    bob_play_hitzone = driver.find_element_by_css_selector('div.bob-play-hitzone')
    bob_play_hitzone.click()


def show_is_upvoted_from_show_preview(driver, show_element):
    """ return true if the show is upvoted AS SEEN FROM THE BOB CONTAINER, False if else"""
    mouse_over_show_if_not_moused_over(driver, show_element)
    #
    try:
        driver.find_element_by_css_selector(
            'div.bob-actions-wrapper a[aria-label="Already rated: thumbs up (click to remove rating)"]'
        )
        return(True)
    except NoSuchElementException:
        return(False)


def show_is_downvoted_from_show_preview(driver, show_element):
    """ return true if the show is downvoted AS SEEN FROM THE BOB CONTAINER, False if else """
    mouse_over_show_if_not_moused_over(driver, show_element)
    #
    try:
        driver.find_element_by_css_selector(
            'div.bob-actions-wrapper a[aria-label="Already rated: thumbs down (click to remove rating)"]'
        )
        return(True)
    except NoSuchElementException:
        return(False)


def upvote_from_show_preview(driver, show_element):
    """ upvote from preview if not upvoted, else do nothing"""
    mouse_over_show_if_not_moused_over(driver, show_element)
    #
    if show_is_upvoted_from_show_preview(driver, show_element):
        print("show is already upvoted, upvote_from_show_preview not executing")
    elif show_is_upvoted_from_show_preview(driver, show_element):
        already_upvoted_button = driver.find_element_by_css_selector(
            'div.bob-actions-wrapper a[aria-label="Already rated: thumbs down (click to remove rating)"]'
        )
        already_upvoted_button.click()
        # HAVE TO WAIT FOR DOWNVOTE UNCLICK TO PROCESS AND FOR THE UPVOTE BUTTON TO APPEAR
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'div.bob-actions-wrapper a[aria-label="Rate thumbs up"]')))
        upvote_button = driver.find_element_by_css_selector(
            'div.bob-actions-wrapper a[aria-label="Rate thumbs up"]'
        )
        upvote_button.click()
    else:
        upvote_button = driver.find_element_by_css_selector(
            'div.bob-actions-wrapper a[aria-label="Rate thumbs up"]'
        )
        upvote_button.click()


def downvote_from_show_preview(driver, show_element):
    """ downvote from preview if not downvoted, else do nothing"""
    mouse_over_show_if_not_moused_over(driver, show_element)
    if show_is_downvoted_from_show_preview(driver, show_element):
        print("show is already downvoted, downvote_from_show_preview not executing")
    elif show_is_upvoted_from_show_preview(driver, show_element):
        already_upvoted_button = driver.find_element_by_css_selector(
            'div.bob-actions-wrapper a[aria-label="Already rated: thumbs up (click to remove rating)"]'
        )
        already_upvoted_button.click()
        # HAVE TO WAIT FOR UPVOTE UNCLICK TO PROCESS AND FOR THE DOWNVOTE BUTTON TO APPEAR
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'div.bob-actions-wrapper a[aria-label="Rate thumbs down"]')))
        downvote_button = driver.find_element_by_css_selector(
            'div.bob-actions-wrapper a[aria-label="Rate thumbs down"]'
        )
        downvote_button.click()
    else:
        downvote_button = driver.find_element_by_css_selector(
            'div.bob-actions-wrapper a[aria-label="Rate thumbs down"]'
        )
        downvote_button.click()


def show_is_in_my_list_from_show_preview(driver, show_element):
    """ """
    mouse_over_show_if_not_moused_over(driver, show_element)
    #
    my_list_button = driver.find_element_by_css_selector(
        'div.bob-actions-wrapper div[data-uia="myListButton"]'
    )
    # I cant find another way to determine if the my list button is checked or not
    # The dom is surprisingly not helpful here. There is not is_checked attribute hidden in an aria
    # tag or anything. I'm going to have to brute force it by mousing over the my_list_button and
    # seeing what the text popup says
    action = ActionChains(driver)
    action.move_to_element(my_list_button).perform()
    status = driver.find_element_by_css_selector(
        'div.bob-actions-wrapper div[data-uia="myListButton"] > span')
    print(f"show status text is {status.text}")
    if status.text == 'Remove from My List':
        return(True)
    else:
        return(False)


def add_show_to_my_list_from_show_preview(driver, show_element):
    """ add show to my list using the bob container. If show already in my list, do nothing"""
    mouse_over_show_if_not_moused_over(driver, show_element)
    if show_is_in_my_list_from_show_preview(driver, show_element):
        print("show already in my list, add_show_to_my_list_from_show_preview not executing")
    else:
        my_list_button = driver.find_element_by_css_selector(
            'div.bob-actions-wrapper div[data-uia="myListButton"]'
        )
        my_list_button.click()


def remove_show_from_my_list_from_show_preview(driver, show_element):
    if not show_is_in_my_list_from_show_preview(driver, show_element):
        print("show isnt in my list already, remove_show_from_my_list_from_show_preview not exe")
    else:
        my_list_button = driver.find_element_by_css_selector(
            'div.bob-actions-wrapper div[data-uia="myListButton"]'
        )
        my_list_button.click()
