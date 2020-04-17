import unittest
import time

from selenium import webdriver

import pagemodels.videopage
import tests.pickledlogin
import secrets
import browserconfig

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


# HELP
# NO IDEA WHAT IM LOOKING AT
# VIDEO EXAMPLE OF EXECUTION:
# https://gyazo.com/37be44a9993676c4161adff157960e45
# https://gyazo.com/e8bb9e87d4793b0ae203cbd54f1a1c73


# TODO- clean up time.sleep()'s. Added as monkeypatches. The underlying VideoPage actions need
# to end with ExpectectedCondition waits. They all passed the smoke tests because they werent
# chained together (and thus nothing was after the last action).


class VideoPageTests(unittest.TestCase):
    """ The following tests test basic use cases for Netflix's video player(dubbed 'Akira player'
    by Netflix). The individual actions are defined at ./pagemodels/videopage.py"""

    @classmethod
    def setUpClass(cls):
        """ launch the webdriver of choice with selected options. (SEE browserconfig.py)
         and then login using pickled cookies. (SEE tests/pickledlogin.py)"""
        cls.driver = browserconfig.driver_runner(
            executable_path=browserconfig.driver_path,
            desired_capabilities=browserconfig.capabilities
        )
        tests.pickledlogin.pickled_login(cls.driver)

    @classmethod
    def tearDownClass(cls):
        """ TODO-"""
        cls.driver.quit()

    def setUp(self):
        """ load some random movie, Minority Report with Tom Cruise in this instance """
        self.driver.get('https://www.netflix.com/watch/80219127?trackId=200254290&tctx=0%2C0%2C3f\
            74b4eb-86f6-4d9d-bb35-a72282cd263c-76893314%2C311384eb-a55b-41d5-bb93-deb09b53bebb_323\
            6856X6XX1587128751673%2C311384eb-a55b-41d5-bb93-deb09b53bebb_ROOT')
        time.sleep(5)  # BUG - TODO- why doesnt webdriver wait here? The page hasnt fully loaded

    # PAUSE TESTS
    def test_pause_from_unpaused_state(self):
        """ from an unpaused state, pause the player"""
        video_page = pagemodels.videopage.VideoPage(self.driver)

        self.assertFalse(
            video_page.player_is_paused(),
            msg="pause_from_unpaused_state wasnt an unpaused state"
        )

        video_page.pause_player()

        self.assertTrue(
            video_page.player_is_paused(),
            msg="pause_from_unpaused_state major test failed"
        )

        # CLEANUP- Netflix's Akira player (annoyingly) remembers the paused state in the next test
        video_page.unpause_player()

    def test_unpause_from_paused_state(self):
        """from a paused state, unpause the player"""
        video_page = pagemodels.videopage.VideoPage(self.driver)
        video_page.pause_player()

        self.assertTrue(
            video_page.player_is_paused(),
            msg="unpause_from_paused_state wasnt paused state"
        )

        video_page.unpause_player()

        self.assertFalse(
            video_page.player_is_paused(),
            msg="unpause_from_paused_state major test failed"
        )

    # MUTE TESTS
    # def test_unmute_from_muted_state(self):
    #     """from a muted state, unmute the player"""
    #     video_page = pagemodels.videopage.VideoPage(self.driver)

    #     video_page.mute_player()

    #     self.assertTrue(
    #         video_page.player_is_muted(),
    #         msg="test_unmute_from_muted_state isnt a muted_state"
    #     )

    #     video_page.unmute_player()

    #     self.assertFalse(
    #         video_page.player_is_muted(),
    #         msg="test_unmute_from_muted_state failed to unmute the player"
    #     )

    # def test_mute_from_unmuted_state(self):
    #     """from an unmuted state, mute the player"""
    #     video_page = pagemodels.videopage.VideoPage(self.driver)

    #     self.assertFalse(
    #         video_page.player_is_muted(),
    #         msg="test_mute_from_unmuted_state isnt an unumuted state"
    #     )

    #     video_page.mute_player()

    #     self.assertTrue(
    #         video_page.player_is_muted(),
    #         msg="test_mute_from_unmuted_state failed to mute the player"
    #     )

#         # CLEANUP
#         video_page.unmute_player()

#     # VOLUME TESTS
    # def test_cut_volume_in_half(self):
    #     """ whatever the current volume is, cut it in half using the volume slider"""
    #     # There is a lot going on under the hood with .get_current_volume() and
    #     # .change_volume_using_percentage() . check out /pagemodels/videopage.py
    #     video_page = pagemodels.videopage.VideoPage(self.driver)

    #     current_volume = video_page.get_current_volume()  # returns a float 0 <= x <= 1

    #     target_volume = current_volume/2
    #     video_page.change_volume_using_percentage(target_volume)
    #     time.sleep(3)

    #     new_volume = video_page.get_current_volume()
    #     self.assertAlmostEqual(new_volume, target_volume, delta=0.02)

    #     # CLEANUP- DEFAULT STATE IS 50% VOLUME
    #     video_page.change_volume_using_percentage(.5)

#     def test_double_volume(self):
#         """ double the current volume (upper limit 100%) using the volume slider"""
#         video_page = pagemodels.videopage.VideoPage(self.driver)

#         current_volume = video_page.get_current_volume()  # float

#         target_volume = current_volume*2
#         if target_volume > 1:
#             # if double the volume is greater than 100%, set target to 100%
#             target_volume = 1
#         video_page.change_volume_using_percentage(target_volume)
#         time.sleep(3)

#         new_volume = video_page.get_current_volume()
#         self.assertAlmostEqual(new_volume, target_volume, delta=0.02)

#     def test_set_volume_to_33_percent(self):
#         """ set the current volume to 33 percent using the volume slider"""
#         video_page = pagemodels.videopage.VideoPage(self.driver)

#         video_page.change_volume_using_percentage(.33)
#         time.sleep(3)

#         new_volume = video_page.get_current_volume()
#         self.assertAlmostEqual(new_volume, .33, delta=.02)

#     # FULLSCREEN TESTS
#     def test_full_screen_from_normal_screen_state(self):
#         """ from a normal_screen state, go full screen"""
#         video_page = pagemodels.videopage.VideoPage(self.driver)
#         self.assertFalse(
#             video_page.player_is_full_screen(),
#             msg="full screen_from_normal_screen was not a normal screen state")
#         video_page.make_full_screen()
#         self.assertTrue(
#             video_page.player_is_full_screen(),
#             msg="full screen_from_normal_screen failed to make the player go full screen")

#     def test_normal_screen_from_full_screen_state(self):
#         """ from a full screen state, go normal screen"""
#         video_page = pagemodels.videopage.VideoPage(self.driver)
#         video_page.make_full_screen()
#         self.assertTrue(
#             video_page.player_is_full_screen(),
#             msg="normal_screen_from_full_screen_state was not a full screen state")
#         video_page.make_normal_screen()
#         self.assertFalse(
#             video_page.player_is_full_screen(),
#             msg="normal_screen_from_full_screen_state failed to make the screen normal screen")

#     # AUDIO AND SUBTITLES TESTS
#     def test_add_subtitles_from_no_subtitles_state(self):
#         """from a state of no subtitles, add english subtitles"""
#         video_page = pagemodels.videopage.VideoPage(self.driver)
#         # adding an extra step here to clean up subtitles from personal use
#         if video_page.has_subtitles():
#             video_page.remove_subtitles()
#         self.assertFalse(
#             video_page.has_subtitles(),
#             msg="add_subitles_from_no_subtitles_state was not a no subtitles state from start,\
#                 THIS COULD HAVE BEEN CAUSED BY PERSONAL VIEWING BY BRADLEY")
#         video_page.add_english_subtitles()
#         self.assertTrue(
#             video_page.has_subtitles(),
#             msg="add_subitles_from_no_subtitles_state failed to add (english) subtitles ")

#         # CLEANUP- Netflix's Akira player remembers subtitles from previous viewings
#         video_page.remove_subtitles()

#     def test_remove_subtitles_from_subtitle_state(self):
#         """from a state with subtitles, remove subtitles"""
#         # DEFAULT STATE IS NO SUBTITLES. CHANGING LANGUAGE FROM ORIGINAL TO OTHER
#         # WILL CAUSE ENGLISH SUBTITLES TO APPEAR FOR ACCOUNTS WITH ENGLISH
#         # THUS IF AUDIO TESTS ARE PERFORMED BEFORE THIS, SUBTITLES MAY OR NOT ALREADY
#         # BE IN THE PASSED-IN-STATE. TODO- BUG
#         video_page = pagemodels.videopage.VideoPage(self.driver)
#         if not video_page.has_subtitles():
#             video_page.add_english_subtitles()
#         self.assertTrue(
#             video_page.has_subtitles(),
#             msg="remove_subtitles_from_subtitle_state was not a subtitle state from start")
#         video_page.remove_subtitles()
#         self.assertFalse(
#             video_page.has_subtitles(),
#             msg="remove_subtitles_from_subtitle_state failed to remove subtitles ")
#         # BUG- removing subtitles pauses/unpauses the player for some reason

#     def test_change_audio_to_spanish_from_english_state(self):
#         """ from english audio state, change to spanish audio"""
#         video_page = pagemodels.videopage.VideoPage(self.driver)
#         # DEFAULT STATE IS ALWAYS ENGLISH
#         current_audio = video_page.get_current_audio()
#         self.assertIn(
#             'nglish',
#             current_audio,
#             msg="test_change_audio_to_spanish_from_english_state wasnt an english state")

#         video_page.change_audio_to_spanish()

#         new_audio = video_page.get_current_audio()
#         self.assertIn(
#             'anish',
#             new_audio,
#             msg="test_change_audio_to_spanish_from_english_state failed to change audio spanish")

#         # CLEANUP
#         time.sleep(3)
#         video_page.change_audio_to_english_original()
#         time.sleep(3)

#     def test_change_audio_to_english_from_spanish_state(self):
#         """ from spanish audio state, change to english audio"""
#         # ENGLISH ORIGINAL NOT ENGLISH. DOESNT WORK ON NON ENGLISH ORIGINAL SHOWS
#         video_page = pagemodels.videopage.VideoPage(self.driver)

#         # DEFAULT STATE IS ALWAYS ENGLISH
#         video_page.change_audio_to_spanish()

#         current_audio = video_page.get_current_audio()
#         self.assertIn(
#             'anish',
#             current_audio,
#             msg="test_change_audio_to_english_from_spanish_state wasnt a Spanish state")

#         time.sleep(3)
#         video_page.change_audio_to_english_original()
#         time.sleep(3)

#         new_audio = video_page.get_current_audio()
#         self.assertIn(
#             'nglish',
#             new_audio,
#             msg="test_change_audio_to_english_from_spanish_state failed to change audio English")

#     # SKIP FORWARD/BACKWARD TESTS
#     def test_skip_forward_30_seconds(self):
#         """ using the skip forwad button, skip forwad 30 seconds"""
#         video_page = pagemodels.videopage.VideoPage(self.driver)

#         current_time = video_page.get_remaining_time_in_seconds()

#         video_page.skip_forward()
#         video_page.skip_forward()
#         video_page.skip_forward()

#         new_time = video_page.get_remaining_time_in_seconds()

#         # WHEN PAUSED, delta < 0.01, WHEN NOT PAUSED AND GOOD CONNECTION, delta < 5
#         self.assertAlmostEqual(current_time + 30, new_time, delta=5)

#     def test_skip_back_30_seconds(self):
#         """ using the skip back button, skip back 30 seconds"""
#         # skipping back at 0:00 will cause the test to fail even though the act of skippin
#         # back three times will not fail
#         video_page = pagemodels.videopage.VideoPage(self.driver)

#         current_time = video_page.get_remaining_time_in_seconds()
#         show_duration = video_page.get_show_duration_in_seconds()
#         self.assertGreater(
#             show_duration-current_time,
#             35,
#             msg="test_skip_back_30_seconds can't skip back when the video isnt even 30 seconds in")
#         video_page.skip_backward()
#         video_page.skip_backward()
#         video_page.skip_backward()

#         new_time = video_page.get_remaining_time_in_seconds()
#         # TODO- CURRENT_TIME and NEW_TIME are not accurate names, they are remaining times really
#         # WHEN PAUSED, delta < 0.01, WHEN NOT PAUSED AND GOOD CONNECTION, delta < 5
#         self.assertAlmostEqual(current_time-30, new_time, delta=5)

#     # TIME/DURATION TESTS
#     def test_go_to_halfway_point(self):
#         """ go to the halfway point in the show/movie using the duration slider"""
#         video_page = pagemodels.videopage.VideoPage(self.driver)

#         video_page.change_to_percentage_time(.5)
#         time.sleep(5)

#         show_duration = video_page.get_show_duration_in_seconds()

#         current_time = video_page.get_remaining_time_in_seconds()
#         print(f" show duration is {show_duration}")
#         print(f"current time is {current_time}")
#         self.assertAlmostEqual(show_duration/2, current_time, delta=10)
#         # Largest observed delta is 6.5 seconds. Not sure what is causing this delta.
#         # seems to be intermittent. Could be the off by a pixel again. BUG- low priority
#         # Maybe it would be eliminated by making a .get_current_time_in_seconds function
#         # instead of relying on .get_remaining_time_in_seconds()

#     # # # # # GO TO CREDITS COMPLICATES THINGS
#     # # # # # TODO- I NEED A  videopage FUCNTIONS TO "watch credits" to redisplay the scrubber
#     # def test_go_to_credits(self):
#     #     """ go to the .98  point in the show/movie USING THE SLIDER"""
#     #     video_page = pagemodels.videopage.VideoPage(self.driver)

#     #     video_page.change_to_percentage_time(.98)

#     #     show_duration = video_page.get_show_duration_in_seconds()

#     #     current_remaining_time = video_page.get_remaining_time_in_seconds()

#     def test_restart_show(self):
#         """ restart a show by setting the percentage_time to 0"""
#         video_page = pagemodels.videopage.VideoPage(self.driver)

#         video_page.change_to_percentage_time(0)

#         time.sleep(3)  # TODO- GET THIS TIME.SLEEP JUNK OUT OF HERE. Chaining tests
#         current_time = video_page.get_remaining_time_in_seconds()
#         show_duration = video_page.get_show_duration_in_seconds()

#         self.assertAlmostEqual(current_time, show_duration, delta=5)

#         # CLEANUP
#         # defualt state can't be 0:00, maybe having halfway point the default state wouldnt be bad
#         video_page.change_to_percentage_time(.5)
#         time.sleep(5)

#     # EXIT PLAYER TESTS
#     def test_exit_player(self):
#         "exit the player by clicking the built-in back arrow button"
#         video_page = pagemodels.videopage.VideoPage(self.driver)
#         video_page.go_back_to_shows()

#         time.sleep(3)  # TODO- clean this up
#         self.assertNotIn('watch', self.driver.current_url)
#         # when watching a show, the url structure is "https://www.netflix.com/watch/600230...""


# # if __name__ == "__main__":
# #     unittest.main()
