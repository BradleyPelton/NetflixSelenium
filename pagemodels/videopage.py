# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

import pagemodels.basepage
# import tests.pickledlogin
# import secrets
# import browserconfig

############################################################################################
# phases of netflix player:
# 0.)loading phase- loading-spinner is present. page is technically finished loading,
# but the player isnt finished loading
# 1.)first idle phase: ui disappars, only video remains
# 2.)second idle phase: title appears, everything gets darker as overlay appears
# 2.5)idle phase 2.5- diplays just the rating. seems to only happen when the video is first played
# 3.)third idle phase- totally idle, you have to click a specific button in the center of the page
# 4.)video is playing, buttons are still being displayed
# 5.)video is playing, buttons are gone (back to idle but video is playing)
# 6.)credits are rolling, video player is made small, recommendations are displayed
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
        self.VOLUME_CONTAINER = (By.CSS_SELECTOR, 'div[data-uia="volume-container"] > button')
        self.VOLUME_SLIDER_CONTAINER = (By.CSS_SELECTOR, 'div.slider-container')
        self.VOLUME_SLIDER = (By.CSS_SELECTOR, 'div.slider-bar-percentage')
        self.VOLUME_S = (By.CSS_SELECTOR, 'div.slider-bar-container')
        self.VOLUME_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Volume"]')
        self.SEEK_BACK_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Seek Back"]')
        self.SEEK_FORWARD_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Seek Forward"]')
        self.TIME_REMAINING = (By.CSS_SELECTOR, 'time.time-remaining__time')
        self.TIME_SCRUBBER = (By.CSS_SELECTOR, 'div[aria-label="Seek time scrubber"]')
        self.TIME_SCRUBBER_BAR = (By.CSS_SELECTOR, 'div.scrubber-bar')
        self.SUBTITLE_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Audio & Subtitles"]')
        self.CURRENT_SUBTITLE_IS_OFF = (
            By.CSS_SELECTOR, 'li.track.selected[data-uia="track-subtitle-Off"]')
        self.SUBTITLE_OFF_BUTTON = (By.CSS_SELECTOR, 'li.track[data-uia="track-subtitle-Off"]')
        self.CURRENT_AUDIO = (
            By.CSS_SELECTOR, 'div.track-list.structural.track-list-audio > ul > li.track.selected')
        self.ENGLISH_SUBTITLE_BUTTON = (By.CSS_SELECTOR, 'li[data-uia="track-subtitle-English"]')
        self.SPANISH_SUBTITLE_BUTTON = (By.CSS_SELECTOR, 'li[data-uia="track-subtitle-Spanish"]')
        self.SPANISH_AUDIO_BUTTON = (By.CSS_SELECTOR, 'li[data-uia="track-audio-Spanish"]')
        self.ENGLISH_AUDIO_BUTTON = (
            By.CSS_SELECTOR, 'li[data-uia="track-audio-English [Original]"]')
        self.SUBTITLE_LANGUAGE_LIST = (
            By.CSS_SELECTOR, 'div.track-list.structural.track-list-subtitles')
        self.HOME_BUTTON = (By.CSS_SELECTOR, 'a[aria-label="Netflix"]')
        self.SPINNER = (By.CSS_SELECTOR, 'div.nf-loading-spinner')

    # IDLE FUNCTIONS
    def initial_spinner_wait(self):
        """When the video page initally loads, the document.readyState event fires before the
        video is ready to play/interact. Not to be confused with video buffering, this is the
        player itself loading."""
        wait = WebDriverWait(self.driver, 10)
        wait.until(
            EC.presence_of_element_located(self.SPINNER),
            message='couldnt find the loading spinner, the page probably failed to load'
        )

        wait = WebDriverWait(self.driver, 10)
        wait.until(
            EC.invisibility_of_element_located(self.SPINNER),
            message='loading spinner never disappeared OR video took too long to load'
        )

    def player_is_idle(self):
        """Return true if player is idle(ui isnt displayed), false if else."""
        try:
            seek_forward_button = self.driver.find_element(*self.SEEK_FORWARD_BUTTON)
            if seek_forward_button.is_displayed():
                # print("player is NOT idle")  # excellent for debugging, but should be removed
                return False
            else:
                # print("player is idle")
                return True
        except NoSuchElementException:
            print(" player_is_idle COULDNT FIND THE SEEK_FORWAD, IS THE PLAYER TOTALLY IDLE???")
            return True

    def wake_up_idle_player(self):
        """Wake up the player if partially idle or totally idle."""
        try:
            # Player is totally idle
            big_play_idle_button = self.driver.find_element(*self.BIG_PLAY_IDLE_BUTTON)
            # print("found big play idle button!")
            big_play_idle_button.click()
        except NoSuchElementException:
            # Player is only partially idle
            # print("couldnt find big play idle button")
            video_player_container = self.driver.find_element(*self.VIDEO_PLAYER_CONTAINER)
            video_player_container.click()  # Click the center of the screen to wake it up

        # WAIT FOR THE PAGE TO COMPLETELY WAKE UP
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located(self.SEEK_FORWARD_BUTTON))

    def wake_up_if_idle(self):
        """Wake up if idle, else do nothing"""
        if self.player_is_idle():
            self.wake_up_idle_player()

    # PAUSE AND UNPAUSE FUNCTIONS
    def player_is_paused(self):
        """Returns true if player is paused, False if player is not-paused(is playing).
        idle does not imply paused. paused does not imply idle. not not paused implies paused."""
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
        """Pause the player if unpaused, else do nothing."""
        if self.player_is_paused():
            print("player is already paused, pause_player is not executing")
        else:
            small_pause_button = self.driver.find_element(*self.SMALL_PAUSE_BUTTON)
            small_pause_button.click()

    def unpause_player(self):
        """Unpause player if paused. if not paused, do nothing."""
        if self.player_is_paused():
            small_play_button = self.driver.find_element(*self.SMALL_PLAY_BUTTON)
            small_play_button.click()
        else:
            print("player is not paused, unpause_player is not executing")

    # MUTED FUNCTIONS
    def player_is_muted(self):
        """Return true if muted, false if else."""
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
        """Mute if unmuted. if already muted, do nothing."""
        # BUG- test fails 10% of the time IF ITS THE FIRST TEST TO BE EXECUTED
        # test always bombs out after failed to find self.MUTED_BUTTON. Not reproducible
        self.wake_up_if_idle()
        if self.player_is_muted():
            print("player is already muted, mute_player not executing")
        else:
            volume_button = self.driver.find_element(*self.VOLUME_BUTTON)
            volume_button.click()

        # Volume slider doesnt close until the user moves the mouse outside of the vol container
        video_player_container = self.driver.find_element(*self.VIDEO_PLAYER_CONTAINER)
        action = ActionChains(self.driver)
        action.move_to_element(video_player_container).perform()

        # Adding a wait until the muted button appears
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located(self.MUTED_BUTTON))

    def unmute_player(self):
        """Unmute player if muted. If alraedy unmuted, do nothing."""
        self.wake_up_if_idle()
        if self.player_is_muted():
            muted_button = self.driver.find_element(*self.MUTED_BUTTON)
            muted_button.click()
        else:
            print("player is already unmuted, unmute_player not executing")

        # Volume slider doesnt close until the user moves the mouse outside of the vol container
        video_player_container = self.driver.find_element(*self.VIDEO_PLAYER_CONTAINER)
        action = ActionChains(self.driver)
        action.move_to_element(video_player_container).perform()  # move the cursor to the center

        # Adding a wait until the volume button(unmuted button) appears
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located(self.VOLUME_BUTTON))

    # VOLUME FUNCTIONS
    def volume_slider_is_open(self):
        """Returns true if the slider is open, false if else."""
        # intentionally not waking up idle player. Idle player implies slider is not open
        try:
            self.driver.find_element(*self.VOLUME_SLIDER)
            return True
        except NoSuchElementException:
            print("volume_slider_is_open couldnt find the volume slider, returning false")
            return False

    def open_volume_slider(self):
        """Hover over the volume button causing the volume slider to open."""
        self.wake_up_if_idle()
        if self.volume_slider_is_open():
            print("volume slider is already open, open_volume slider is not executing")
        volume_container = self.driver.find_element(*self.VOLUME_CONTAINER)
        # volume_container is a container for the volume button, NOT THE SLIDER
        action = ActionChains(self.driver)
        action.move_to_element(volume_container).perform()
        # wait for the slider to appear
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located(self.VOLUME_SLIDER_CONTAINER))

    def open_volume_slider_if_not_open(self):
        """Opens slider if not open, if open do nothing."""
        if self.volume_slider_is_open():
            print("volume slider is already open, open_volume_slider_if_not_open not executing")
        else:
            self.open_volume_slider()

    def get_current_volume(self) -> float:
        """Return the current volume as a float 0 <= x <= 1 , 1 being max volume, 0 being muted."""
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
        """Change the volume to a percentage
        e.g. volume_percentage =.5 means 50% volume, .25 = 25% volume etc.
        BUG- off by 1 pixel. See below
        """
        self.open_volume_slider_if_not_open()
        volume_slider = self.driver.find_element(*self.VOLUME_S)
        action_2 = ActionChains(self.driver)
        # action_2.move_to_element(volume_slider).click().perform()  # always moves to the center
        # MOVE_TO_ELEMENT_WITH_OFFSET OFFSETS RELATIVE TO THE TOP LEFT CORNER OF ELEMENT
        y_offset = volume_slider.size['height'] * (1-desired_volume_percentage)
        action_2.move_to_element_with_offset(
            volume_slider, 0, y_offset    # volume_bar.size['height']*volume_percentage
            ).click().perform()

        # Volume slider doesnt close until the user moves the mouse outside of the vol container
        video_player_container = self.driver.find_element(*self.VIDEO_PLAYER_CONTAINER)
        action = ActionChains(self.driver)
        action.move_to_element(video_player_container).perform()  # move the cursor to the center

        # BUG- volume seems to be off by .0133756 percent, a little over a single pixel
        # Not sure whats causing it. Test using change_volume_using_percentage and
        # get_current_volume

    #  FULL SCREEN FUCNTIONS
    def player_is_full_screen(self):
        """Return true if full screen. A player is always either full screen or normal screen."""
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
        """Make full screen if not full screen. If full screen, do nothing."""
        self.wake_up_if_idle()
        if self.player_is_full_screen():
            print("player is already full screen! not executing make_full_screen")
        else:
            full_screen_button = self.driver.find_element(*self.FULL_SCREEN_BUTTON)
            full_screen_button.click()

    def make_normal_screen(self):
        """Make normal_screen if player is full screen. If normal screen already, do nothing."""
        self.wake_up_if_idle()
        if not self.player_is_full_screen():
            print("player is already normal screen, make_normal_screen not executing")
        else:
            normal_screen = self.driver.find_element(*self.NORMAL_SCREEN_BUTTON)
            normal_screen.click()

    # SUBTITLE & AUDIO LANGUAGE FUNCTIONS
    def subtitle_menu_is_open(self):
        """Return true if the subtitle menu is open, false if else."""
        # Intentionally not waking up player. Idle player means menu is not open.
        try:
            self.driver.find_element(*self.ENGLISH_SUBTITLE_BUTTON)
            return True  # TODO- MINOR BUG - not all shows will have english subtitles
        except NoSuchElementException:
            return False

    def open_subtitle_menu_if_not_open(self):
        """Open subtitle menu if it is not already open. If it is open, do nothing."""
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
        """Return true if the player has subtitles, false if else."""
        self.wake_up_idle_player()
        self.open_subtitle_menu_if_not_open()
        try:
            self.driver.find_element(*self.CURRENT_SUBTITLE_IS_OFF)
            return False
        except NoSuchElementException:
            return True

    def remove_subtitles(self):
        """Remove the subtiles by clicking the subtitles_off choice."""
        self.wake_up_if_idle()
        self.open_subtitle_menu_if_not_open()

        subtitles_off_button = self.driver.find_element(*self.SUBTITLE_OFF_BUTTON)
        subtitles_off_button.click()

    def add_english_subtitles(self):
        """Add english subtitles to a show."""
        self.wake_up_if_idle()
        self.open_subtitle_menu_if_not_open()

        english = self.driver.find_element(*self.ENGLISH_SUBTITLE_BUTTON)
        english.click()

    def get_current_audio(self):
        """Return a str of the current audio language."""
        self.wake_up_idle_player()
        self.open_subtitle_menu_if_not_open()

        currently_selected_audio = self.driver.find_element(*self.CURRENT_AUDIO)
        return currently_selected_audio.text

    def change_audio_to_english_original(self):
        """Change the audio to english."""
        # NOTE- There is a difference between English audio and English[Audio Description] and
        # English[Original].
        self.wake_up_idle_player()
        self.open_subtitle_menu_if_not_open()

        english_audio_button = self.driver.find_element(*self.ENGLISH_AUDIO_BUTTON)
        english_audio_button.click()

        # Subtitle Menu doesnt close until the user moves the mouse outside of the menu
        video_player_container = self.driver.find_element(*self.VIDEO_PLAYER_CONTAINER)
        action = ActionChains(self.driver)
        action.move_to_element(video_player_container).perform()  # move the cursor to the center

        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.invisibility_of_element_located(self.ENGLISH_AUDIO_BUTTON))

    def change_audio_to_spanish(self):
        """Change the AUDIO language to spanish."""
        self.wake_up_if_idle()
        self.open_subtitle_menu_if_not_open()

        spanish_audio_button = self.driver.find_element(*self.SPANISH_AUDIO_BUTTON)
        spanish_audio_button.click()

        # Subtitle menu doesnt close until the user moves the mouse outside of the menu
        video_player_container = self.driver.find_element(*self.VIDEO_PLAYER_CONTAINER)
        action = ActionChains(self.driver)
        action.move_to_element(video_player_container).perform()  # move the cursor to the center

        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.invisibility_of_element_located(self.SPANISH_AUDIO_BUTTON))

    # SKIP FUNCTIONS
    def skip_backward(self):
        """Rewind the player 10 seconds using the seek back button, while paused or unpaused."""
        self.wake_up_if_idle()

        seek_back_button = self.driver.find_element(*self.SEEK_FORWARD_BUTTON)
        seek_back_button.click()
        # BUG- FORWARD = BACKWARD FOR SOME REASON IN THE DOM. REVERSED HERE ON PURPOSE.

    def skip_forward(self):
        """Skip forward 10 seconds using the seek forward button, while paused or unpaused."""
        self.wake_up_if_idle()

        seek_forward_button = self.driver.find_element(*self.SEEK_BACK_BUTTON)
        seek_forward_button.click()
        # BUG- FORWARD = BACKWARD FOR SOME REASON IN THE DOM. REVERSED HERE ON PURPOSE.

    # TIME/DURATION FUNCTIONS
    def get_remaining_time_in_seconds(self):
        """Returns the amount of time left in current show as displayed in the bottom right
        corner. NOTE- see get_show_duration. This could be refactored to use seek_time_scrubber."""
        self.wake_up_if_idle()
        time_remaining = self.driver.find_element(*self.TIME_REMAINING)
        if time_remaining.text == '':
            print("get_remaining_time failed, maybe the player was idle???")
            return time_remaining.text
        else:
            show_duration_list = time_remaining.text.split(":")
            show_duration_in_seconds = (
                                    int(show_duration_list[0])*3600
                                    + int(show_duration_list[1])*60
                                    + int(show_duration_list[2])
            )
            return show_duration_in_seconds

    def get_show_duration(self) -> str:
        """Return a str 'HH:MM:SS' that represents a shows TOTAL duration."""
        # No need to wake the player, value is always present(but not visible).
        seek_time_scrubber = self.driver.find_element(*self.TIME_SCRUBBER)
        scrubber_value = seek_time_scrubber.get_attribute('aria-valuetext').split(" ")
        # e.g. of scrubber_value ['1:02', 'of', '25:42']
        # BUG- If the show is less than an hour, show_duration_list[0] is minutes not hours.
        assert len(scrubber_value) == 3, "get_show_duration SCRUBBER_VALUE found extra values"
        return scrubber_value[2]

    def get_show_duration_in_seconds(self) -> int:
        """Return the number of seconds in a show/movie."""
        # No need to wake the player, value is always present(but not visible).
        seek_time_scrubber = self.driver.find_element(*self.TIME_SCRUBBER)
        scrubber_value = seek_time_scrubber.get_attribute('aria-valuetext').split(" ")
        # e.g. of scrubber_value ['1:02', 'of', '25:42']
        assert len(scrubber_value) == 3, "get_show_duration SCRUBBER_VALUE found extra values"
        # BUG- If the show is less than an hour, show_duration_list[0] is minutes not hours.
        show_duration_list = scrubber_value[2].split(":")
        show_duration_in_seconds = (
                                int(show_duration_list[0])*3600
                                + int(show_duration_list[1])*60
                                + int(show_duration_list[2])
        )
        return show_duration_in_seconds

    def change_to_percentage_time(self, percentage_left: float):
        """Change the time left in the show to percentage_left, a float. e.g. .5 for 50%,
        .25 for 25%, .1 for 10%.
        """
        self.wake_up_if_idle()
        time_scrubber_bar = self.driver.find_element(*self.TIME_SCRUBBER_BAR)

        action = ActionChains(self.driver)
        action.move_to_element_with_offset(
            time_scrubber_bar, time_scrubber_bar.size['width']*percentage_left, 0).perform()
        action.click().perform()

        video_player_container = self.driver.find_element(*self.VIDEO_PLAYER_CONTAINER)
        action2 = ActionChains(self.driver)
        action2.move_to_element(video_player_container).perform()  # move the cursor to the center

    def change_to_exact_time(self, hours, minutes, seconds):
        """User provides a time in the movie they want to navigate to (e.g. 1 hour, 35 minutes,
        20 seconds). This function converts that to a percentage of the movie left, then uses
        change_to_percentage_time function.
        """
        # TODO- Seems to be a +- 1 second difference. Im guessing its the fault of floating point
        # arithemetic not representing the exact_time_as_percentage. Could also be  padding/margin
        # of the scrubber element by the browser. 1 second difference BUG- low priority

        show_duration = self.get_show_duration()  # returns a str 'HH:MM:SS'
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

    # BACK FUNCTIONS
    def go_back_to_shows(self):
        """Use the back button located inside of the player to return to the previous show list."""
        self.wake_up_if_idle()
        back_button = self.driver.find_element(*self.BACK_BUTTON)
        back_button.click()

        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located(self.HOME_BUTTON))

    ##################################################################################
    # FUCNTIONS THAT DIDNT MAKE THE FIRST CUT

    # REPORT FUNCTIONS
    # def report_issue(self):
    #     """ It was once considered to add the ability to automate the process of reporting issues
    #     After consideration, the possibility of it being used for nefarious acts against Netflix
    #     led to this function being scrapped """
    #     pass

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

    # CREDITS FUCNTIONS
    # def view_credits(self):
    #     """ When the credits appear, the player will shrink to 10% of its size and the page will
    #     be dominated by an add for "What to watch next"""

    #     # There is something complicated going on here
    #     # The player still exists, but it is 10% of its normal size
    #     # b.click() doesnt work but neither does click any other node
    #     # TODO
    #     b = driver.find_element_by_css_selector('div.PlayerControlsNeo__all-controls')

    #     action = ActionChains(driver)
    #     action.move_to_element(b).click(b).perform()

    # def upvote_from_credits(self):
    #     pass

    # def downvote_from_credits(self):
    #     pass

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

    # def get_current_time(self):
    #     """ TODO"""
    #     pass

