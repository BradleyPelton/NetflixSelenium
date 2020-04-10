import unittest

from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException

import pagemodels.videopage
import tests.logintests

login_container = tests.logintests.LoginTests()
login_container.user_login_main()
# TODO- rename this. its not a login_container


class VideoPageTests(unittest.TestCase):
    """ The following tests test basic user stories for Netflix's video player(dubbed Akira player
    by Netflix). The individual actions are defined at ./pagemodels/videopage.py"""
    # NOTE- KEEP TESTS IN A USER-FRIENDLY ORDER, people are lazy and dont read more than a few
    # lines

    def __init__(self):
        self.driver = login_container.driver

    def wake_up(self):
        """wake up"""
        video_page = pagemodels.videopage.VideoPage(self.driver)
        video_page.wake_up_idle_player()

    # PAUSE TESTS
    def pause_from_unpaused_state(self):
        """ from unpaused state, pause the player"""
        video_page = pagemodels.videopage.VideoPage(self.driver)
        assert not video_page.player_is_paused(), "pause_from_unpaused_state wasnt unpaused state"
        video_page.pause_player()
        assert video_page.player_is_paused(), "pause_from_unpaused_state major test failed"
        # TODO- there is duplicate logic here. pause_player() already checks if state is already
        # paused. I could delete it there or let it double check. I'm electing for the latter 
    
    def unpause_from_paused_state(self):
        """from a paused state, unpause the player"""
        video_page = pagemodels.videopage.VideoPage(self.driver)
        assert  video_page.player_is_paused(), "unpause_from_paused_state wasnt paused state"
        video_page.unpause_player()
        assert not video_page.player_is_paused(), "unpause_from_paused_state major test failed"
        # TODO- there is duplicate logic here. pause_player() already checks if state is already
        # paused. I could delete it there or let it double check. I'm electing for the latter
    
    # MUTE TESTS
    def unmute_from_muted_state(self):
        """from a muted state, unmute the player"""
        video_page = pagemodels.videopage.VideoPage(self.driver)
        assert video_page.player_is_muted(), "unmute_from_muted_state isnt a muted_state"
        video_page.unmute_player()
        assert not video_page.player_is_muted(), "unmute_from_muted_state failed to unmute the \
            player"

    def mute_from_unmuted_state(self):
        """from an unmuted state, mute the player"""
        video_page = pagemodels.videopage.VideoPage(self.driver)
        assert not video_page.player_is_muted(), "mute_from_unmuted_state isnt an unumuted state"
        video_page.mute_player()
        assert video_page.player_is_muted(), "mute_from_unmuted_state failed to mute the player"
    
    # VOLUME TESTS
    # def cut_volume_in_half(self):
    #     assert new_volume < volume/2

    # FULLSCREEN TESTS
    def full_screen_from_normal_screen_state(self):
        """ from a normal_screen state, go full screen"""
        video_page = pagemodels.videopage.VideoPage(self.driver)
        assert not video_page.player_is_full_screen(), "full screen_from_normal_screen was not a \
            normal screen state"
        video_page.make_full_screen()
        assert video_page.player_is_full_screen(), "full screen_from_normal_screen failed to make \
            the player go full screen"

    def normal_screen_from_full_screen_state(self):
        """ from a full screen state, go normal screen"""
        video_page = pagemodels.videopage.VideoPage(self.driver)
        assert video_page.player_is_full_screen(), "normal_screen_from_full_screen_state was not \
            a full screen state"
        video_page.make_normal_screen()
        assert not video_page.player_is_full_screen(), "normal_screen_from_full_screen_state \
            failed to make the screen normal screen"

    # AUDIO AND SUBTITLES TESTS
    def add_subtitles_from_no_subtitles_state(self):
        """from a state of no subtitles, add english subtitles"""
        video_page = pagemodels.videopage.VideoPage(self.driver)
        assert not video_page.has_subtitles(), "add_subitles_from_no_subtitles_state was not a no \
            subtitles state from start"
        video_page.add_english_subtitles()
        assert video_page.has_subtitles(), "add_subitles_from_no_subtitles_state failed to add \
            (english) subtitles "

    def remove_subtitles_from_subtitle_state(self):
        """from a state with subtitles, remove subtitles"""
        video_page = pagemodels.videopage.VideoPage(self.driver)
        assert video_page.has_subtitles(), "remove_subtitles_from_subtitle_state was not a \
            subtitle state from start"
        video_page.remove_subtitles()
        assert not video_page.has_subtitles(), "remove_subtitles_from_subtitle_state failed to \
            remove subtitles "
        # BUG- removing subtitles pauses/unpauses the player for some reason

    # TIME TESTS
    def skip_forward_30_seconds(self):
        # TODO- NOT FUNCTIONAL. FIX
        video_page = pagemodels.videopage.VideoPage(self.driver)

        current_time = video_page.get_remaining_time_in_seconds()

        video_page.skip_forward()
        video_page.skip_forward()
        video_page.skip_forward()

        new_time = video_page.get_remaining_time_in_seconds()

        assert current_time + 29 < new_time and \
            current_time + 31 > new_time, "skip_forward_30_seconds test failed"

    def skip_back_30_seconds(self):
        """ skipping back at 0:00 will cause the test to fail even though the act of skippin
        back three times will not fail.  """
        # TODO- NOT FUNCTIONAl. FIX
        video_page = pagemodels.videopage.VideoPage(self.driver)

        current_time = video_page.get_remaining_time_in_seconds()

        video_page.skip_backward()
        video_page.skip_backward()
        video_page.skip_backward()

        new_time = video_page.get_remaining_time_in_seconds()

        assert current_time - 29 > new_time and \
            current_time - 31 < new_time, "skip_back_30_seconds test failed"




b = pagemodels.videopage.VideoPage(login_container.driver)
# a = VideoPageTests()
