import unittest
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import pagemodels.videopage
import tests.pickledlogin
import secrets


# TEST CATEGORIES
# 1.) Pause Tests
# 2.) Mute Tests
# 3.) Volume Tests
# 4.) Full screen Tests
# 5.) Audio&Subtitles Tests
# 6.) Skip_forward/backward Tests
# 7.) Time/Duration Tests
# 8.) Exit Player Tests
# NICE-TO-HAVES
# 9.) Keyboard shortcuts TODO- 'f' for fullscreen, 'm' for mute


class VideoPageTests(unittest.TestCase):
    """ The following tests test basic user cases for Netflix's video player(dubbed 'Akira player'
    by Netflix). The individual actions are defined at ./pagemodels/videopage.py"""

    @classmethod
    def setUpClass(cls):
        chromedriver_path = secrets.chromedriver_path
        self.driver = webdriver.Chrome(executable_path=chromedriver_path)
        tests.pickledlogin.pickled_login()

        # load some random movie, Minority Report with Tom Cruise in this instance
        self.driver.get('https://www.netflix.com/watch/60023071?trackId=14170286&tctx=2%2C1%2C\
            fc2cbd3b-8737-4f69-9a21-570f1a21a1a3-42400306%2C3f5aa22b-d569-486c-b94d-a8503e6725\
            ae_22068878X3XX1586569622702%2C3f5aa22b-d569-486c-b94d-a8503e6725ae_ROOT')

    def tearDownClass(cls):
        """ TODO-"""
        driver.quit()

    # PAUSE TESTS
    def test_pause_from_unpaused_state(self):
        """ from unpaused state, pause the player"""
        video_page = pagemodels.videopage.VideoPage(self.driver)
        self.assertFalse(
            video_page.player_is_paused(),
            msg="pause_from_unpaused_state wasnt unpaused state")
        video_page.pause_player()
        self.assertTrue(
            video_page.player_is_paused(),
            msg="pause_from_unpaused_state major test failed")

    def test_unpause_from_paused_state(self):
        """from a paused state, unpause the player"""
        video_page = pagemodels.videopage.VideoPage(self.driver)
        self.assertTrue(
            video_page.player_is_paused(),
            msg="unpause_from_paused_state wasnt paused state")
        video_page.unpause_player()
        self.assertFalse(
            video_page.player_is_paused(),
            msg="unpause_from_paused_state major test failed")
        # TODO- there is duplicate logic here. pause_player() already checks if state is already
        # paused. I could delete it there or let it double check. I'm electing for the latter

    # MUTE TESTS
    def test_unmute_from_muted_state(self):
        """from a muted state, unmute the player"""
        video_page = pagemodels.videopage.VideoPage(self.driver)
        self.assertTrue(
            video_page.player_is_muted(),
            msg="unmute_from_muted_state isnt a muted_state")
        video_page.unmute_player()
        self.assertFalse(
            video_page.player_is_muted(),
            msg="unmute_from_muted_state failed to unmute the player")

    def test_mute_from_unmuted_state(self):
        """from an unmuted state, mute the player"""
        video_page = pagemodels.videopage.VideoPage(self.driver)
        self.asserFalse(
            video_page.player_is_muted(),
            msg="mute_from_unmuted_state isnt an unumuted state")
        video_page.mute_player()
        self.assertTrue(
            video_page.player_is_muted(),
            msg="mute_from_unmuted_state failed to mute the player")

    # VOLUME TESTS
    def test_cut_volume_in_half(self):
        """ whatever the current volume is, cut it in half USING THE VOLUME SLIDER"""
        # There is a lot going on under the hood with .get_current_volume() and
        # .change_volume_using_percentage() . check out /pagemodels/videopage.py if curious
        video_page = pagemodels.videopage.VideoPage(self.driver)

        current_volume = video_page.get_current_volume()  # float

        target_volume = current_volume/2
        video_page.change_volume_using_percentage(target_volume)

        new_volume = video_page.get_current_volume()
        self.assertEqual(new_volume, target_volume, delta=.02)

    def test_double_volume(self):
        """ double the current volume (upper limit 100%) USING THE VOLUME SLIDER"""
        video_page = pagemodels.videopage.VideoPage(self.driver)

        current_volume = video_page.get_current_volume()  # float

        target_volume = current_volume*2
        if target_volume > 1:
            # if double the volume is greater than 100%, set target to 100%
            target_volume = 1
        video_page.change_volume_using_percentage(target_volume)

        new_volume = video_page.get_current_volume()
        video_page.assertEqual(new_volume, target_volume, delta=.02)

    def test_set_volume_to_33_percent(self):
        """ set the current volume to 33 percent USING THE VOLUME SLIDER"""
        video_page = pagemodels.videopage.VideoPage(self.driver)

        video_page.change_volume_using_percentage(.33)

        new_volume = video_page.get_current_volume()
        video_page.assertEqual(new_volume, .33, delta=.02)

    # FULLSCREEN TESTS
    def test_full_screen_from_normal_screen_state(self):
        """ from a normal_screen state, go full screen"""
        video_page = pagemodels.videopage.VideoPage(self.driver)
        self.assertFalse(
            video_page.player_is_full_screen(),
            msg="full screen_from_normal_screen was not a normal screen state")
        video_page.make_full_screen()
        self.assertTrue(
            video_page.player_is_full_screen(),
            msg="full screen_from_normal_screen failed to make the player go full screen")

    def test_normal_screen_from_full_screen_state(self):
        """ from a full screen state, go normal screen"""
        video_page = pagemodels.videopage.VideoPage(self.driver)
        self.assertTrue(
            video_page.player_is_full_screen(),
            msg="normal_screen_from_full_screen_state was not a full screen state")
        video_page.make_normal_screen()
        self.assertFalse(
            video_page.player_is_full_screen(),
            msg="normal_screen_from_full_screen_state failed to make the screen normal screen")

    # AUDIO AND SUBTITLES TESTS
    def test_add_subtitles_from_no_subtitles_state(self):
        """from a state of no subtitles, add english subtitles"""
        video_page = pagemodels.videopage.VideoPage(self.driver)
        self.assertFalse(
            video_page.has_subtitles(),
            msg="add_subitles_from_no_subtitles_state was not a no subtitles state from start")
        video_page.add_english_subtitles()
        self.assertTrue(
            video_page.has_subtitles(),
            msg="add_subitles_from_no_subtitles_state failed to add (english) subtitles ")

    def test_remove_subtitles_from_subtitle_state(self):
        """from a state with subtitles, remove subtitles"""
        video_page = pagemodels.videopage.VideoPage(self.driver)
        self.assertTrue(
            video_page.has_subtitles(),
            msg="remove_subtitles_from_subtitle_state was not a subtitle state from start")
        video_page.remove_subtitles()
        self.assertFalse(
            video_page.has_subtitles(),
            msg="remove_subtitles_from_subtitle_state failed to remove subtitles ")
        # BUG- removing subtitles pauses/unpauses the player for some reason

    def test_change_audio_to_spanish_from_english_state(self):
        video_page = pagemodels.videopage.VideoPage(self.driver)

        current_audio = video_page.get_current_audio()
        self.assertIn(
            'nglish',
            current_audio,
            msg="test_change_audio_to_spanish_from_english_state wasnt an english state")

        video_page.change_audio_to_spanish()

        new_audio = video_page.get_current_audio()
        self.assertIn(
            'anish',
            new_audio,
            msg="test_change_audio_to_spanish_from_english_state failed to change audio spanish")

    def test_change_audio_to_english_from_spanish_state(self):
        """ ENGLISH ORIGINAL NOT ENGLISH. DOESNT WORK ON NON ENGLISH ORIGINAL SHOWS """
        video_page = pagemodels.videopage.VideoPage(self.driver)

        current_audio = video_page.get_current_audio()
        self.assertIn(
            'anish',
            current_audio,
            msg="test_change_audio_to_english_from_spanish_state wasnt a Spanish state")

        video_page.change_audio_to_english_original()

        new_audio = video_page.get_current_audio()
        self.assertIn(
            'nglish',
            new_audio,
            msg="test_change_audio_to_english_from_spanish_state failed to change audio English")

    # SKIP FORWARD/BACKWARD TESTS
    def test_skip_forward_30_seconds(self):
        """ """
        video_page = pagemodels.videopage.VideoPage(self.driver)

        current_time = video_page.get_remaining_time_in_seconds()

        video_page.skip_forward()
        video_page.skip_forward()
        video_page.skip_forward()

        new_time = video_page.get_remaining_time_in_seconds()

        self.assertAlmostEqual(current_time + 30, new_time, delta=1)

    def test_skip_back_30_seconds(self):
        """ skipping back at 0:00 will cause the test to fail even though the act of skippin
        back three times will not fail.  """
        video_page = pagemodels.videopage.VideoPage(self.driver)

        current_time = video_page.get_remaining_time_in_seconds()

        video_page.skip_backward()
        video_page.skip_backward()
        video_page.skip_backward()

        new_time = video_page.get_remaining_time_in_seconds()
        # TODO- CURRENT_TIME and NEW_TIME are not accurate names, they are remaining times really
        self.assertAlmostEqual(current_time-30, new_time, delta=1)

    # TIME/DURATION TESTS
    def test_go_to_halfway_point(self):
        """ go to the halfway point in the show/movie USING THE SLIDER"""
        video_page = pagemodels.videopage.VideoPage(self.driver)

        video_page.change_to_percentage_time(.5)

        show_duration = video_page.get_show_duration_in_seconds()

        current_time = video_page.get_remaining_time_in_seconds()
        # print(f" show duration is {show_duration}")
        # print(f"current time is {current_time}")
        self.assertAlmostEqual(show_duration/2, current_time, delta=10)
        # Largest observed delta is 6.5 seconds. Not sure what is causing this delta.
        # seems to be intermittent. Could be the off by a pixel again. BUG- low priority
        # Maybe it would be eliminated by making a .get_current_time_in_seconds function
        # instead of relying on .get_remaining_time_in_seconds()

    def test_go_to_credits(self):
        """ go to the .98  point in the show/movie USING THE SLIDER"""
        video_page = pagemodels.videopage.VideoPage(self.driver)

        video_page.change_to_percentage_time(.98)

        show_duration = video_page.get_show_duration_in_seconds()

        current_remaining_time = video_page.get_remaining_time_in_seconds()
        # print(f" show duration is {show_duration}")
        # print(f"current time is {current_time}")
        self.assertAlmostEqual(show_duration*.02, current_remaining_time, delta=10)
        # Largest observed delta is 6.5 seconds. Not sure what is causing this delta.
        # seems to be intermittent. Could be the off by a pixel again. BUG- low priority
        # Maybe it would be eliminated by making a .get_current_time_in_seconds function
        # instead of relying on .get_remaining_time_in_seconds()

    def test_restart_show(self):
        """ restart a show by setting the percentage_time to 0"""
        video_page = pagemodels.videopage.VideoPage(self.driver)

        video_page.change_to_percentage_time(0)

        time.sleep(3)  # TODO- GET THIS TIME.SLEEP JUNK OUT OF HERE. Chaining tests
        current_time = video_page.get_remaining_time_in_seconds()
        show_duration = video_page.get_show_duration_in_seconds()

        self.assertAlmostEqual(current_time, show_duration, delta=1)

    # EXIT PLAYER TESTS
    def test_exit_player(self):
        "exit the player by clicking the built-in back arrow button"
        video_page = pagemodels.videopage.VideoPage(self.driver)
        video_page.go_back_to_shows()

        time.sleep(3)  # TODO- clean this up
        self.assertNotIn('watch', self.driver.current_url)
        # when watching a show, the url structure is "https://www.netflix.com/watch/600230...""


if __name__ == "__main__":
    unittest.main()
