import time
from collections import defaultdict

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


from login import driver, user_login
import secrets
import mylisttools
import showtools
import genrepagetools

### this page will house all of the functions for the VIDEO PAGE
### NAME TBD
### the page in which you actually stream the video content

# NETFLIX CALLS THE PLAYER THE nfp AkiraPlayer. netflix player AkiraPlayer?



############################################################################################
############################################################################################
############################################################################################
############################################################################################
# PHASES:

# ACTIVE
# FIRST IDLE PHASE: UI DISAPPARS, ONLY VIDEO REMAINS
# SECOND IDLE PHASE: TITLE APPEARS, EVERYTHING GETS DARKER AS OVERLAY APPEARS

# IDLE PHASE 1.5????- diplays just the rating. Seems to only happen when the video is first played

# TOTALLY IDLE, YOU HAVE TO CLICK A SPECIFIC BUTTON IN THE CENTER OF THE PAGE TO 

# VIDEO IS PLAYING, BUTTONS ARE STILL BEING DISPLAYED
# VIDEO IS PLAYING, BUTTONS ARE GONE (BACK TO IDLE BUT VIDEO IS PLAYING)

############################################################################################
############################################################################################
############################################################################################
############################################################################################




def add_english_subtitles():
    pass


def remove_subtitles():
    pass

def change_all_settings(**KWARGS):
    """ change to full screen, add subtitles, max volume, and any other options user wants"""
    pass


def player_is_idle(driver):
    """ return bool is player is idle"""
    """ if player is playing, it is considered idle"""
    """ IDLE IF AND ONLY IF BUTTONS ARE BEING DISPLAYED"""
    # TODO- change the definition of idle? maybe player_is_showing_buttons ? palyer_is_showing_UI ?
    seek_forward_button = driver.find_element_by_css_selector('button[aria-label="Seek Forward"]')
    if seek_forward_button.is_displayed():
        print(" player is NNNNOOOOOTTTT idle")
        return(False)  # VIDEO PLAYER IS NOT IDLE
    else:
        print("player is idle")
        return(True)   # VIDEO PLAY IS IDLE


def wake_up_idle_player(driver):
    """buttons are gone with idle"""
    video_player_container = driver.find_element_by_css_selector('div.nfp.AkiraPlayer')
    video_player_container.click()  # Click the center of the screen to wake it up
    # WAIT FOR THE PAGE TO COMPLETELY WAKE UP
    wait = WebDriverWait(driver,10)
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, 'button[aria-label="Seek Forward"]')))


def wake_up_if_idle(driver):
    """ ADD THIS TO EVERY FUNCTION THE SAME WAY I HAVE "OPEN JAWBONE IF NOT OPEN" WITH SHOWTOOLS"""
    if player_is_idle(driver):
        wake_up_idle_player(driver)


def player_is_paused(driver):
    """PAUSED IS IRREGARDLESS OF IDLE. IDLE DOES NOT IMPLY PAUSED
    A PLAYER IS ALWAYS PAUSED OR NOT PAUSED. THUS NOT NOT PAUSED IMPLIES PAUSED """
    wake_up_if_idle(driver)
    try:
        small_play_button = driver.find_element_by_css_selector('button[aria-label="Play"]')
        return True
    except NoSuchElementException:
        pass
        # print("could not find small play button during player_is_paused")
    try:
        small_pause_button = driver.find_element_by_css_selector('button[aria-label="Pause"]')
        return False
    except:
        print("player_is_paused couldnt find either play nor pause button, SOMETHING IS WRONG")


def unpause_player(driver):
    """ unpause player if paused. if not paused, do nothing """
    wake_up_if_idle(driver)
    if player_is_paused(driver):
        print("PAUSED")
        small_play_button = driver.find_element_by_css_selector('button[aria-label="Play"]')
        small_play_button.click()
    else:
        print("player is not paused, unpause_player is not executing")


def get_remaining_time(driver):
    """ returns the amount of time left in this specific show"""
    """ NOT TESTED, TODO- Test"""
    wake_up_if_idle(driver)
    time_remaining = driver.find_element_by_css_selector('time.time-remaining__time')
    if time_remaining.text == '':
        print("GET_REMAINING_TIME FAILED, MAYBE THE PLAYER WAS IDLE???")
        return(time_remaining.text)
    else:
        return(time_remaining.text)


def player_is_fullscreen(driver):
    """ this requires 'waking up' the player. TODO- See if its possible to not wake up"""
    """ A PLAYER IS ALWAYS EITHER FULL SCREEN OR NORMAL SCREEN. THUS NOT FULL SCREEN IMPLIES NORMAL
    """
    wake_up_if_idle(driver)
    # CASE 1- I CAN FIND THE FULL SCREEN BUTTON
    try:
        full_screen_button = driver.find_element_by_css_selector('button[aria-label="Full screen"]')
        return(False)
    except NoSuchElementException:
        print("couldnt find the full screen button")
    # CASE 2- I CAN FIND THE SMALLSCREEN BUTTON
    try:
        normal_screen = driver.find_element_by_css_selector('button[aria-label="Exit full screen"]')
        return(True)
    except NoSuchElementException:
        print("player_is_fullscreen couldnt find either buttons, SOMETHING IS WRONG")


def make_fullscreen(driver):
    """ make fullscreen if not fullscreen. if fullscreen, do nothing"""
    wake_up_if_idle(driver)  # TODO- DUPLICATE WAKE UPS, SEE ABOUT FIING THIS
    if player_is_fullscreen(driver):
        print("player is already fullscreen! not executing make_fullscreen")
    else:
        full_screen_button = driver.find_element_by_css_selector('button[aria-label="Full screen"]')
        full_screen_button.click()


def make_normal_screen(driver):
    """ make normal_screen if player is fullscreen. if normal screen already, do nothing"""
    wake_up_if_idle(driver)  # TODO- DUPLICATE WAKE UPS, SEE ABOUT FIING THIS
    if not player_is_fullscreen(driver):
        print("player is already normal screen, make_normal_screen not executing")
    else:
        normal_screen = driver.find_element_by_css_selector('button[aria-label="Exit full screen"]')
        normal_screen.click()



# video_player_container = driver.find_element_by_css_selector('div.nfp.AkiraPlayer')
# video_player_cotainer.click()


# stops working after the first execution, research ActionChains
# from selenium.webdriver.common.action_chains import ActionChains
# action = ActionChains(driver)
# action.move_to_element(video_player_cotainer).perform()



# ALL OF THE FOLLOWING BUTTONS WORK
back_arrow = driver.find_element_by_css_selector('button[data-uia="nfplayer-exit"]')
back_arrow.click

small_play_button = driver.find_element_by_css_selector('button[aria-label="Play"]')
small_play_button.click()

seek_back_button = driver.find_element_by_css_selector('button[aria-label="Seek Back"]')
seek_back_button.click()

seek_forward_button = driver.find_element_by_css_selector('button[aria-label="Seek Forward"]')
seek_forward_button.click()


volume_button = driver.find_element_by_css_selector('button[aria-label="Volume"]')
volume_button.click()  # Clicking the volume button mutes and unmutes the video, also adds slider

title = driver.find_element_by_css_selector('h4.ellipsize-text')
print(title.text)

report_problem_button = driver.find_element_by_css_selector(
    'button[aria-label="Report a problem with playback to Netflix."')
report_problem_button.click()  #clicking launches report modal, double clicking doesnt close

subtitles_button = driver.find_element_by_css_selector('button[aria-label="Audio & Subtitles"]')
subtitles_button.click()  #clicking launches the subtitles modal, but clicking again doesnt close 

full_screen_button = driver.find_element_by_css_selector('button[aria-label="Full screen"]')
full_screen_button.click()  # Functions as both "make fullscreen" and "make small screen"



