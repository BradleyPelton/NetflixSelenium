import time
from collections import defaultdict

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from login import driver, user_login
import secrets
import mylisttools
import showtools
import genrepagetools

### this page will house all of the functions for the VIDEO PAGE
### NAME TBD
### the page in which you actually stream the video content

# NETFLIX CALLS THE PLAYER THE nfp AkiraPlayer. netflix player AkiraPlayer?

# FULL XPATH TO THE BUTTONS
/html/body/div[1]/div/div/div[1]/div/div/div[2]/div/div[3]/div/div[5]/div[2]/div[2]/button[1]

# testing the player is a giant pain in the ass

############################################################################################
############################################################################################
############################################################################################
############################################################################################
# PHASES:
### ACTIVELY HOVERING OVER, VIDEO PAUSED
### ACTIVELY HOVERING OVER, VIDEO PLAYING

# PARTIAL IDLE , diplays just the rating. Seems to only happen when the video is first played
#

### COMPLETELY IDLE, not mouse activity in 5 seconds
############################################################################################
############################################################################################
############################################################################################
############################################################################################



def pause_video():
    pass


def play_video_after_pause():
    pass

def add_english_subtitles():
    pass


def remove_subtitles():
    pass

def change_all_settings(**KWARGS):
    """ change to full screen, add subtitles, max volume, and any other options user wants"""
    pass

def make_fullscreen(driver):
    """ make full screen. If already full screen, do nothing"""

def wake_up_idle_player(driver):
    """buttons are gone with idle"""
    video_player_container = driver.find_element_by_css_selector('div.nfp.AkiraPlayer')
    video_player_cotainer.click()


def player_is_idle(driver):
    """ return bool is player is idle"""
    """ NOT TESTED, TODO- VERY IMPORTANT, TEST THIS"""
    small_play_button = driver.find_element_by_css_selector('button[aria-label="Play"]')
    if small_play_button.is_displayed():
        print(" player is NNNNOOOOOTTTT idle")
        return(False)  # VIDEO PLAYER IS NOT IDLE
    else:
        print("player is idle")
        return(True)   # VIDEO PLAY IS IDLE

def wake_up_if_idle(driver):
    """ ADD THIS TO EVERY FUNCTION THE SAME WAY I HAVE "OPEN JAWBONE IF NOT OPEN" WITH SHOWTOOLS"""
    pass

def player_is_paused(driver):
    pass


def get_remaining_time(driver):
    """ returns the amount of time left in this specific show"""
    """ NOT TESTED, TODO- Test"""
    time_remaining = driver.find_element_by_css_selector('time.time-remaining__time')
    return(time_remaining.text)

for _ in range(20):
video_player_cotainer = driver.find_element_by_css_selector('div.nfp.AkiraPlayer')
video_player_cotainer.click()
    time.sleep(5)



video_player_container = driver.find_element_by_css_selector('div.nfp.AkiraPlayer')
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




