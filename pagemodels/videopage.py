import unittest
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


import pagemodels.basepage
import tests.pickledlogin
import secrets

# NETFLIX CALLS THE PLAYER THE nfp AkiraPlayer. netflix player AkiraPlayer?

############################################################################################
# PHASES:

# ACTIVE
# FIRST IDLE PHASE: UI DISAPPARS, ONLY VIDEO REMAINS
# SECOND IDLE PHASE: TITLE APPEARS, EVERYTHING GETS DARKER AS OVERLAY APPEARS

# IDLE PHASE 1.5- diplays just the rating. Seems to only happen when the video is first played

# THIRD IDLE PHASE- TOTALLY IDLE, YOU HAVE TO CLICK A SPECIFIC BUTTON IN THE CENTER OF THE PAGE

# VIDEO IS PLAYING, BUTTONS ARE STILL BEING DISPLAYED
# VIDEO IS PLAYING, BUTTONS ARE GONE (BACK TO IDLE BUT VIDEO IS PLAYING)

# CREDITS ARE ROLLING, VIDEO PLAYER IS MADE SMALL, RECOMMENDATIONS ARE DISPLAYED
# TODO- I DID NOT ACCOUNT FOR THIS!!!! TODO- NEED TO FACTOR THIS IN AS WELL
# HAPPENS AFTER change_time_using_slidebar(.99)
############################################################################################

# Function CATEGORIES
# 0.) Idle functions
# 1.) Pause functions
# 2.) Mute functions
# 3.) Volume functions
# 4.) Full screen functions
# 5.) Audio&Subtitles functions
# 6.) Skip_forward/backward functions
# 7.) Time/Duration functions
# 8.) Exit Player functions




# # # # DELETE ME 
# chromedriver_path = secrets.chromedriver_path
# driver = webdriver.Chrome(executable_path=chromedriver_path)
# tests.pickledlogin.pickled_login(driver)


# driver.get('https://www.netflix.com/watch/60023071?trackId=14170286&tctx=2%2C1%2C\
#     fc2cbd3b-8737-4f69-9a21-570f1a21a1a3-42400306%2C3f5aa22b-d569-486c-b94d-a8503e6725\
#     ae_22068878X3XX1586569622702%2C3f5aa22b-d569-486c-b94d-a8503e6725ae_ROOT')


class VideoPage(pagemodels.basepage.BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # LOCATORS
        self.VIDEO_PLAYER_CONTAINER = (By.CSS_SELECTOR, 'div.nfp.AkiraPlayer')
        self.BIG_PLAY_IDLE_BUTTON = (By.CSS_SELECTOR, 'div.PlayView-play > div > button')
        self.BACK_BUTTON = (By.CSS_SELECTOR, 'button[data-uia="nfplayer-exit"]')
        self.SMALL_PLAY_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Play"]')
        self.SMALL_PAUSE_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Pause"]')
        self.FULL_SCREEN_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Full screen"]')
        self.NORMAL_SCREEN_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Exit full screen"]')
        self.MUTED_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Muted"]')
        self.VOLUME_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Volume"]')
        self.VOLUME_SLIDER = (By.CSS_SELECTOR, 'div.slider-bar-percentage')
        self.VOLUME_CONTAINER = (By.CSS_SELECTOR, 'div[data-uia="volume-container"]')
        self.SEEK_BACK_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Seek Back"]')
        self.SEEK_FORWARD_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Seek Forward"]')
        self.TIME_REMAINING = (By.CSS_SELECTOR, 'time.time-remaining__time')
        self.TIME_SCRUBBER = (By.CSS_SELECTOR, 'div[aria-label="Seek time scrubber"]')
        self.TIME_SCRUBBER_BAR = (By.CSS_SELECTOR, 'div.scrubber-bar')
        self.SUBTITLE_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Audio & Subtitles"]')
        self.CURRENT_SUBTITLE_IS_OFF = (By.CSS_SELECTOR, 'li.track.selected[data-uia="track-subtitle-Off"]')
        self.SUBTITLE_OFF_BUTTON = (By.CSS_SELECTOR, 'li.track[data-uia="track-subtitle-Off"]')
        self.CURRENT_AUDIO = (By.CSS_SELECTOR, 'div.track-list.structural.track-list-audio > ul > li.track.selected')
        self.ENGLISH_SUBTITLE_BUTTON = (By.CSS_SELECTOR, 'li[data-uia="track-subtitle-English"]')
        self.SPANISH_SUBTITLE_BUTTON = (By.CSS_SELECTOR, 'li[data-uia="track-subtitle-Spanish"]')
        self.SPANISH_AUDIO_BUTTON = (By.CSS_SELECTOR, 'li[data-uia="track-audio-Spanish"]')
        self.ENGLISH_AUDIO_BUTTON = (By.CSS_SELECTOR, 'li[data-uia="track-audio-English [Original]"]')
        self.SUBTITLE_LANGUAGE_LIST = (By.CSS_SELECTOR, 'div.track-list.structural.track-list-subtitles')

    # IDLE FUNCTIONS
    def player_is_idle(self):
        """ return bool is player is idle. If player is playing, it is considered idle
            IDLE IF AND ONLY IF BUTTONS ARE BEING DISPLAYED.
            INITIAL IDLE COUNTS AS IDLE"""
        try:
            seek_forward_button = self.driver.find_element(*self.SEEK_FORWARD_BUTTON)
            if seek_forward_button.is_displayed():
                print("player is NOT idle")  # TODO- excellent for debugging, but should be removed
                return False
            else:
                print("player is idle")
                return True
        except NoSuchElementException:
            print(" player_is_idle COULDNT FIND THE SEEK_FORWAD, IS THE PLAYER TOTALLY IDLE???")
            return True


    def wake_up_idle_player(self):
        """ TODO- BUG- if player is TOTALLY idle, no activity in several minutes, this wont wake.
        when player is totally idle, a small play button appears in the center of the page"""
        try:
            big_play_idle_button = self.driver.find_element(*self.BIG_PLAY_IDLE_BUTTON)
            print("found big play idle button!")
            big_play_idle_button.click()
        except NoSuchElementException:
            print("couldnt find big play idle button")
            video_player_container = self.driver.find_element(*self.VIDEO_PLAYER_CONTAINER)
            video_player_container.click()  # Click the center of the screen to wake it up
        # WAIT FOR THE PAGE TO COMPLETELY WAKE UP
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located(self.SEEK_FORWARD_BUTTON))

    def wake_up_if_idle(self):
        """ wake up if idle, else do nothing"""
        if self.player_is_idle():
            self.wake_up_idle_player()

    # PAUSE AND UNPAUSE FUNCTIONS
    def player_is_paused(self):
        """Returns true if player is paused, False if player is not-paused(is playing).
        PAUSED IS IRREGARDLESS OF IDLE. IDLE DOES NOT IMPLY PAUSED
        A PLAYER IS ALWAYS PAUSED OR NOT PAUSED. THUS NOT NOT PAUSED IMPLIES PAUSED """
        self.wake_up_if_idle()
        try:
            self.driver.find_element(*self.SMALL_PLAY_BUTTON)
            return True
        except NoSuchElementException:
            pass
            # print("could not find small play button during player_is_paused")
        try:
            self.driver.find_element(*self.SMALL_PAUSE_BUTTON)
            return False
        except NoSuchElementException:
            print("player_is_paused couldnt find either play nor pause button, SOMETHING IS WRONG")

    def pause_player(self):
        """ self-explanatory """
        self.wake_up_if_idle()
        if self.player_is_paused():
            print("player is already paused, pause_player is not executing")
        else:
            small_pause_button = self.driver.find_element(*self.SMALL_PAUSE_BUTTON)
            small_pause_button.click()

    def unpause_player(self):
        """ unpause player if paused. if not paused, do nothing """
        self.wake_up_if_idle()
        if self.player_is_paused():
            small_play_button = self.driver.find_element(*self.SMALL_PLAY_BUTTON)
            small_play_button.click()
        else:
            print("player is not paused, unpause_player is not executing")

    # MUTED FUNCTIONS
    def player_is_muted(self):
        """ return true if muted, false if else"""
        self.wake_up_if_idle()
        try:
            self.driver.find_element(*self.MUTED_BUTTON)
            return True
        except NoSuchElementException:
            pass
        try:
            self.driver.find_element(*self.VOLUME_BUTTON)
            return False
        except NoSuchElementException:
            pass
        print("player_is_muted couldnt find either the muted or volume button. SOMETHING IS WRONG")

    def mute_player(self):
        """ mute if unmuted. if already muted, do nothing"""
        """ BUG- mute_player causes the volume slider to open and never close"""
        self.wake_up_if_idle()
        if self.player_is_muted():
            print("player is already muted, mute_player not executing")
        else:
            volume_button = self.driver.find_element(*self.VOLUME_BUTTON)
            volume_button.click()
            # small problem appeared. Muted the player causes the volume bar to stay open for
            # TODO- CLEAN THIS UP

    def unmute_player(self):
        """ unmute player if muted. If alraedy unmuted, do nothing"""
        self.wake_up_if_idle()
        if self.player_is_muted():
            muted_button = self.driver.find_element(*self.MUTED_BUTTON)
            muted_button.click()
            # small problem appeared. Muted the player causes the volume bar to stay open for
            # TODO- CLEAN THIS UP
        else:
            print("player is already unmuted, unmute_player not executing")

    # VOLUME FUNCTIONS
    def volume_slider_is_open(self):
        """ returns true if the slider is open, false if else"""
        # intentionally not waking up idle player. Idle player implies slider is not open
        self.wake_up_if_idle()
        try:
            self.driver.find_element(*self.VOLUME_SLIDER)
            return True
        except NoSuchElementException:
            print("volume_slider_is_open couldnt find the volume slider, returning false")
            return False

    def open_volume_slider(self):
        """ hover over the volume button causing the volume slider to open"""
        """ TODO- TEST NEED TO TEST ALL VOLUME STATES (low,medium,high, muted) """
        self.wake_up_if_idle()
        if self.volume_slider_is_open():
            print("volume slider is already open, open_volume slider is not executing")
        time.sleep(3)
        volume_container = self.driver.find_element(*self.VOLUME_CONTAINER)
        action = ActionChains(self.driver)
        action.move_to_element(volume_container).perform()
        # wait for the slider to appear
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.slider-container')))
        # TODO- slider-container was never identified. See if VOLUME_CONTAINER or other works

    def open_volume_slider_if_not_open(self):
        """ opens slider if not open, if open do nothing"""
        if self.volume_slider_is_open():
            print("volume slider is already open, open_volume_slider_if_not_open not executing")
        else:
            self.open_volume_slider()

    def get_current_volume(self) -> float:
        """ TODO"""
        self.open_volume_slider_if_not_open()
        if self.player_is_muted():
            return 0.0
        volume_percentage = self.driver.find_element(*self.VOLUME_SLIDER)
        # naturally, volume_percentage returns the percentage in a nasty format
        # volume_percentage.get_attribute('style')  returns 'height: 45.4094%;'
        str_volume = volume_percentage.get_attribute('style').split(" ")[-1]
        str_volume = str_volume[:-2]
        float_volume = (float(str_volume)/100)
        return float_volume

    def change_volume_using_percentage(self, desired_volume_percentage: float):
        """ change the volume to a percentage
        e.g. volume_percentage =.5 means 50% volume, .25 = 25% volume etc.
        TODO- off by 1 pixel BUG. See below
        """
        self.open_volume_slider_if_not_open()
        volume_slider = self.driver.find_element(*self.VOLUME_SLIDER)
        action_2 = ActionChains(self.driver)
        # action_2.move_to_element(volume_slider).click().perform()  # always moves to the center
        # MOVE_TO_ELEMENT_WITH_OFFSET OFFSETS RELATIVE TO THE TOP LEFT CORNER OF ELEMENT
        y_offset = volume_slider.size['height'] * (1-desired_volume_percentage)
        action_2.move_to_element_with_offset(
            volume_slider, 0, y_offset    # volume_bar.size['height']*volume_percentage
            ).click().perform()
        # BUG- volume seems to be off by .0133756 percent, a little over a single pixel
        # Not sure whats causing it. Test using change_volume_using_percentage and
        # get_current_volume

    #  FULL SCREEN FUCNTIONS
    def player_is_full_screen(self):
        """ A PLAYER IS ALWAYS EITHER FULL SCREEN OR NORMAL SCREEN. THUS NOT FULL SCREEN IMPLIES
        NORMAL SCREEN
        """
        self.wake_up_if_idle()
        try:
            self.driver.find_element(*self.FULL_SCREEN_BUTTON)
            return False
        except NoSuchElementException:
            print("couldnt find the full screen button")
        try:
            self.driver.find_element(*self.NORMAL_SCREEN_BUTTON)
            return True
        except NoSuchElementException:
            print("player_is_full_screen couldnt find either buttons, SOMETHING IS WRONG")

    def make_full_screen(self):
        """ make full screen if not full screen. if full screen, do nothing"""
        self.wake_up_if_idle()  # TODO- DUPLICATE WAKE UPS, SEE ABOUT FIXING THIS
        if self.player_is_full_screen():
            print("player is already full screen! not executing make_full_screen")
        else:
            full_screen_button = self.driver.find_element(*self.FULL_SCREEN_BUTTON)
            full_screen_button.click()

    def make_normal_screen(self):
        """ make normal_screen if player is full screen. if normal screen already, do nothing"""
        self.wake_up_if_idle()  # TODO- DUPLICATE WAKE UPS, SEE ABOUT FIING THIS
        if not self.player_is_full_screen():
            print("player is already normal screen, make_normal_screen not executing")
        else:
            normal_screen = self.driver.find_element(*self.NORMAL_SCREEN_BUTTON)
            normal_screen.click()

    # SUBTITLE & AUDIO LANGUAGE FUNCTIONS
    def subtitle_menu_is_open(self):
        """ return true if the subtitle menu is open, false if else"""
        """ TODO- CLEAN THIS UP"""
        # INTENTIONALLY NOT WAKING UP PLAYER. IDLE PLAYER MEANS MENU IS NOT OEPN
        try:
            self.driver.find_element(*self.ENGLISH_SUBTITLE_BUTTON)
            return True  # TODO- MINOR BUG - not all shows will have english subtitles
        except NoSuchElementException:
            return False  # SLOPPY CODE. OTHER CASES EXIST, BAD TRY EXCEPT

    def open_subtitle_menu_if_not_open(self):
        """ open subtitle menu if it is not already open. If it is open, do nothing"""
        self.wake_up_if_idle()
        if self.subtitle_menu_is_open():
            print("subtitle menu is already open, open_subtitle_menu_if_not_open isnt executing")
        else:
            subtitles_button = self.driver.find_element(*self.SUBTITLE_BUTTON)
            subtitles_button.click()
            # wait until the menu is open
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'div.track-list.structural.track-list-subtitles')))
            # never used again, leaving the raw CSS SELECTOR in there

    def has_subtitles(self):
        self.wake_up_idle_player()
        self.open_subtitle_menu_if_not_open()
        try:
            self.driver.find_element(*self.CURRENT_SUBTITLE_IS_OFF)
            return False
        except NoSuchElementException:
            return True

    def remove_subtitles(self):
        """ return true if the player already has subtitles enabled (OF ANY LANGUAGE).
        False if else"""
        """ TODO- UNTESTED"""
        self.wake_up_if_idle()
        self.open_subtitle_menu_if_not_open()
        #
        assert self.has_subtitles()
        subtitles_off_button = self.driver.find_element(*self.SUBTITLE_OFF_BUTTON)
        subtitles_off_button.click()
        # BUG- UNPAUSES PLAYER, but it does remove subtitles

    def add_english_subtitles(self):
        # TODO- IT WORKS BUT SEEMS SKETCHY. NEEDS TO BE TESTED. I THOUGHT SINCE THE SUBTITLE MODAL
        # WAS ALREADY OPENT THA OPENING IT AGAIN WITH SUBTITLES_BUTTON.CLICK() WAS GOING TO CAUSE A
        # PROBLEM. INVESTIGATE
        self.wake_up_if_idle()
        self.open_subtitle_menu_if_not_open()
        english = self.driver.find_element(*self.ENGLISH_SUBTITLE_BUTTON)
        english.click()

    def get_current_audio(self):
        """ assert that the audio is currently english
        NOTE- THERE IS A DIFFERENCE BETWEEN English audio and English[Audio Description
        """
        self.wake_up_idle_player()
        self.open_subtitle_menu_if_not_open()

        currently_selected_audio = self.driver.find_element(*self.CURRENT_AUDIO)
        return currently_selected_audio.text

    def change_audio_to_english_original(self):
        """NOTE- THERE IS A DIFFERENCE BETWEEN English audio and English[Audio Description] and
        English[Original] . For the sake of consistency, this test suite will only focus on english
        only shows until refactored for other languages.
        """
        self.wake_up_idle_player()
        self.open_subtitle_menu_if_not_open()
        english_audio_button = self.driver.find_element(*self.ENGLISH_AUDIO_BUTTON)
        english_audio_button.click()

    def change_audio_to_spanish(self):
        """spoken language != subtitles. This function changes the verbal language to spanish"""
        """not fully tested, TODO-TEST"""
        self.wake_up_if_idle()
        self.open_subtitle_menu_if_not_open()
        spanish_audio_button = self.driver.find_element(*self.SPANISH_AUDIO_BUTTON)
        spanish_audio_button.click()

    # def change_audio_to_original_language(self):
        # for li in ul:
        #     if 'original' in li.text:
        #         li.click()

    # def change_spoken_language(driver , language):
    #     """ going to add this to the "nice to have" category. Not pressing."""
    #     """ TODO- GENERALIZATION FUCNTION takes in language: str and changes the spoken
    #     language to that language"""
    #     pass

    # def change_all_settings(**KWARGS):
    #     """ a super function that takes in a list of options and performs them"""

    # SKIP FUNCTIONS
    def skip_backward(self):
        """ rewind the player 10 seconds using the seek back button. PAUSED OR UNPAUSED"""
        self.wake_up_if_idle()
        #
        seek_back_button = self.driver.find_element(*self.SEEK_FORWARD_BUTTON)
        seek_back_button.click()
        # BUG- FORWARD = BACKWARD FOR SOME REASON IN THE DOM. REVERSED HERE ON PURPOSE. DEBUG

    def skip_forward(self):
        """ skip forward 10 seconds using the seek forward button.  PAUSED OR UNPAUSED"""
        self.wake_up_if_idle()
        #
        seek_forward_button = self.driver.find_element(*self.SEEK_BACK_BUTTON)
        seek_forward_button.click()
        # BUG- FORWARD = BACKWARD FOR SOME REASON IN THE DOM. REVERSED HERE ON PURPOSE. DEBUG

    # TIME/DURATION FUNCTIONS
    def get_remaining_time_in_seconds(self):
        """ returns the amount of time left in this specific show AS DISPLAYED IN THE BOTTOM RIGHT
        CORNER. NOTE- see get_show_duration . This could be refactored to use seek_time_scrubber"""
        """ NOT TESTED, TODO- Test"""
        self.wake_up_if_idle()
        time_remaining = self.driver.find_element(*self.TIME_REMAINING)
        if time_remaining.text == '':
            print("GET_REMAINING_TIME FAILED, MAYBE THE PLAYER WAS IDLE???")
            return time_remaining.text
        else:
            show_duration_list = time_remaining.text.split(":")
            show_duration_in_seconds = (
                                    int(show_duration_list[0])*3600
                                    + int(show_duration_list[1])*60
                                    + int(show_duration_list[2])
            )
            return show_duration_in_seconds

    def get_current_time(self):
        """ TODO"""
        pass

    def get_show_duration(self) -> str:
        """ return a str  'HH:MM:SS' """
        # no need to wake the
        seek_time_scrubber = self.driver.find_element(*self.TIME_SCRUBBER)
        scrubber_value = seek_time_scrubber.get_attribute('aria-valuetext').split(" ")
        # TODO- Add an example of what scrubber_value is supposed to look like
        assert len(scrubber_value) == 3, "get_show_duration SCRUBBER_VALUE found extra values"
        return scrubber_value[2]

    def get_show_duration_in_seconds(self) -> int:
        """ return the number of seconds in a show/movie"""
        # no need to wake the
        seek_time_scrubber = self.driver.find_element(*self.TIME_SCRUBBER)
        scrubber_value = seek_time_scrubber.get_attribute('aria-valuetext').split(" ")
        # TODO- Add an example of what scrubber_value is supposed to look like
        assert len(scrubber_value) == 3, "get_show_duration SCRUBBER_VALUE found extra values"
        # print(scrubber_value)
        show_duration_list = scrubber_value[2].split(":")
        show_duration_in_seconds = (
                                int(show_duration_list[0])*3600
                                + int(show_duration_list[1])*60
                                + int(show_duration_list[2])
        )
        return show_duration_in_seconds

    def change_to_percentage_time(self, percentage_left: float):
        """
        INPUT:
        percentage_left: float     e.g. .5 for 50%, .25 for 25%, .1 for 10%
        NOTE- NETFLIX CALLS THIS THE SCRUBBER?
        THIS IS THE BIG ONE. THE HARD PROBLEM.
        NOTE- Even If I could change the position by editing the html, thats not really testing the
        functionality of the slider. I need to use mouse locations to mimic user behavior
        """
        self.wake_up_if_idle()
        time_scrubber_bar = self.driver.find_element(*self.TIME_SCRUBBER_BAR)
        action = ActionChains(self.driver)
        action.move_to_element_with_offset(
            time_scrubber_bar, time_scrubber_bar.size['width']*percentage_left, 0).perform()
        action.click().perform()

    def change_to_exact_time(self, hours, minutes, seconds):
        """ User provides a time in the movie they want to navigate to
            e.g. 1 hour, 35 minutes, 20 seconds
            This function converts that to a percentage of the movie left, then uses
            change_to_percentage_time
        """
        """ TODO- Seems to be a +- 1 second difference. Im guessing its the fault of floating point
        arithemetic not representing the exact_time_as_percentage. COULD ALSO BE  PADDING/MARGIN
        OF THE SCRUBBER ELEMENT BY THE BROWSER. 1 second difference BUG categorized as low priority
        """
        show_duration = self.get_show_duration()  # return  s a str 'HH:MM:SS'
        show_duration_list = show_duration.split(":")
        show_duration_in_seconds = (
                                    int(show_duration_list[0])*3600
                                    + int(show_duration_list[1])*60
                                    + int(show_duration_list[2])
        )
        exact_time_in_seconds = int(hours)*3600 + int(minutes)*60 + int(seconds)
        print(exact_time_in_seconds, show_duration_in_seconds)
        exact_time_as_percentage = exact_time_in_seconds / show_duration_in_seconds
        print(exact_time_as_percentage)
        self.change_to_percentage_time(exact_time_as_percentage)

    # REPORT FUNCTIONS
    # def report_issue(self):
    #     """ It was once considered to add the ability to automate the process of reporting issues
    #     After consideration, the possibility of it being used for nefarious acts against Netflix
    #     led to this function being scrapped """
    #     pass

    # BACK FUNCTIONS
    def go_back_to_shows(self):
        """ use the back button located inside of the player to return to the previous show list"""
        self.wake_up_if_idle()
        back_button = self.driver.find_element(*self.BACK_BUTTON)
        back_button.click()

    # SKIP FUNCTIONS
    # def skip_intro(driver):
    #     """ during the into/OP of some shows, Netflix will display a "Skip Intro" button
    #     The button can appear 5 seconds into the show or 5 minute into the show. This presents
    # quite a problem for Selenium because we dont have full async functionality since we depend on
    # the webdriver API. Tools like https://arsenic.readthedocs.io/en/latest/ promise to help, but
    #  it seems like a lot of work for a "Nice-to-have" feature. TODO- NICE TO HAVE"""
    #     pass
    # def skip_recap(driver):
        # """very similar to skip_intro but with the "Skip Recap" button. See '7 deadly sins'"""
