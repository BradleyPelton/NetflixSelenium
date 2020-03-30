import time
from selenium.common.exceptions import NoSuchElementException



def show_has_saved_progress(driver, show_element, JAWBONE_OPEN=False) -> bool:
    """ CHECK IF SHOW HAS SAVED PROGRESS, if so return False, else False"""
    if JAWBONE_OPEN:
        print("show_has_saved_progress was told JAWBONE WAS OPEN")
    else:
        print("show_has_saved-Progress is opening the JAWBONE")
        show_element.click()
        time.sleep(3)
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

def get_maturity_rating(driver,show_element, JAWBONE_OPEN=False) -> str:
    """ return the maturity rating for a show, E.G. 'PG', 'PG-13', 'TV-MA'"""
    pass

def get_show_match_percentage(driver,show_element, JAWBONE_OPEN=False) -> int:
    """ returns the match percentage e.g. '99% Match' for Castlevania"""
    pass

def get_release_date():
    pass

def get_number_of_seasons_and_episodes():
    pass

def upvote_show():
    pass

def downvote_show():
    pass

def is_upvoted():
    pass

def is_downvoted():
    pass
