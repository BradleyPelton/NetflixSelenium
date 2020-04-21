import unittest

import pagemodels.videopage
import tests.pickledlogin
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
# 9.) Keyboard shortcuts TODO- 'f' for fullscreen, 'm' for mute, etc.


# HELP
# NO IDEA WHAT IM LOOKING AT
# VIDEO EXAMPLE OF EXECUTION:
# https://gyazo.com/7c703e6bba5af706849052df65772089


class VideoPageTests(unittest.TestCase):
    """The following tests test basic use cases for Netflix's video player(dubbed 'Akira player'
    by Netflix). The individual actions are defined at ./pagemodels/videopage.py"""

    @classmethod
    def setUpClass(cls):
        """Launch the webdriver of choice with selected options(see browserconfig.py).
        Then login using pickled cookies(see tests/pickledlogin.py)."""
        if browserconfig.current_browser in ['chrome', 'firefox']:
            cls.driver = browserconfig.driver_runner(
                executable_path=browserconfig.driver_path,
                desired_capabilities=browserconfig.capabilities
            )
        elif browserconfig.current_browser == 'edge':
            cls.driver = browserconfig.driver_runner(
                executable_path=browserconfig.driver_path,
                desired_capabilities=browserconfig.capabilities
            )
        tests.pickledlogin.pickled_login(cls.driver)

    @classmethod
    def tearDownClass(cls):
        """Closes the browser and shuts down the driver executable."""
        cls.driver.quit()

    def setUp(self):
        """Load some random movie, Avengers: Infinity War in this instance."""
        self.driver.get('https://www.netflix.com/watch/80219127?trackId=200254290&tctx=0%2C0%2C3f\
            74b4eb-86f6-4d9d-bb35-a72282cd263c-76893314%2C311384eb-a55b-41d5-bb93-deb09b53bebb_32\
            36856X6XX1587128751673%2C311384eb-a55b-41d5-bb93-deb09b53bebb_ROOT')
        video_page = pagemodels.videopage.VideoPage(self.driver)
        video_page.initial_spinner_wait()  # Wait for the player to load

    # PAUSE TESTS
    def test_pause_from_unpaused_state(self):
        """From an unpaused state, pause the player."""
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

        # CLEANUP- Netflix's Akira player remembers the paused state in the next test.
        video_page.unpause_player()

    def test_unpause_from_paused_state(self):
        """From a paused state, unpause the player."""
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
    def test_unmute_from_muted_state(self):
        """From a muted state, unmute the player."""
        video_page = pagemodels.videopage.VideoPage(self.driver)
        video_page.mute_player()

        self.assertTrue(
            video_page.player_is_muted(),
            msg="test_unmute_from_muted_state isnt a muted_state"
        )

        video_page.unmute_player()

        self.assertFalse(
            video_page.player_is_muted(),
            msg="test_unmute_from_muted_state failed to unmute the player"
        )

    def test_mute_from_unmuted_state(self):
        """From an unmuted state, mute the player."""
        video_page = pagemodels.videopage.VideoPage(self.driver)

        self.assertFalse(
            video_page.player_is_muted(),
            msg="test_mute_from_unmuted_state isnt an unumuted state"
        )

        video_page.mute_player()

        self.assertTrue(
            video_page.player_is_muted(),
            msg="test_mute_from_unmuted_state failed to mute the player"
        )

        # CLEANUP
        video_page.unmute_player()

    # VOLUME TESTS
    def test_cut_volume_in_half(self):
        """Whatever the current volume is, cut it in half using the volume slider."""
        # There is a lot going on under the hood with .get_current_volume() and
        # .change_volume_using_percentage() . Check out /pagemodels/videopage.py
        video_page = pagemodels.videopage.VideoPage(self.driver)

        current_volume = video_page.get_current_volume()  # returns a float 0 <= x <= 1

        target_volume = current_volume/2
        video_page.change_volume_using_percentage(target_volume)

        new_volume = video_page.get_current_volume()
        self.assertAlmostEqual(new_volume, target_volume, delta=0.02)

        # CLEANUP- default state is 50% volume
        video_page.change_volume_using_percentage(.5)

    def test_double_volume(self):
        """Double the current volume (upper limit 100%) using the volume slider."""
        video_page = pagemodels.videopage.VideoPage(self.driver)

        current_volume = video_page.get_current_volume()  # returns a float 0 <= x <= 1

        target_volume = current_volume*2
        if target_volume > 1:
            # if double the volume is greater than 100%, set target to 100%
            target_volume = 1
        video_page.change_volume_using_percentage(target_volume)

        new_volume = video_page.get_current_volume()
        self.assertAlmostEqual(new_volume, target_volume, delta=0.02)

    def test_set_volume_to_33_percent(self):
        """Set the current volume to 33 percent using the volume slider."""
        video_page = pagemodels.videopage.VideoPage(self.driver)

        video_page.change_volume_using_percentage(.33)

        new_volume = video_page.get_current_volume()
        self.assertAlmostEqual(new_volume, .33, delta=.02)

    # FULLSCREEN TESTS
    def test_full_screen_from_normal_screen_state(self):
        """From a normal_screen state, go full screen."""
        video_page = pagemodels.videopage.VideoPage(self.driver)

        self.assertFalse(
            video_page.player_is_full_screen(),
            msg="full screen_from_normal_screen was not a normal screen state"
        )

        video_page.make_full_screen()

        self.assertTrue(
            video_page.player_is_full_screen(),
            msg="full screen_from_normal_screen failed to make the player go full screen"
        )

    def test_normal_screen_from_full_screen_state(self):
        """From a full screen state, go normal screen."""

        video_page = pagemodels.videopage.VideoPage(self.driver)
        video_page.make_full_screen()

        self.assertTrue(
            video_page.player_is_full_screen(),
            msg="normal_screen_from_full_screen_state was not a full screen state"
        )

        video_page.make_normal_screen()

        self.assertFalse(
            video_page.player_is_full_screen(),
            msg="normal_screen_from_full_screen_state failed to make the screen normal screen"
        )

    # AUDIO AND SUBTITLES TESTS
    def test_add_subtitles_from_no_subtitles_state(self):
        """From a state of no subtitles, add english subtitles."""
        video_page = pagemodels.videopage.VideoPage(self.driver)
        # adding an extra step here to clean up subtitles from personal use
        if video_page.has_subtitles():
            video_page.remove_subtitles()

        self.assertFalse(
            video_page.has_subtitles(),
            msg="add_subitles_from_no_subtitles_state was not a no subtitles state from start,\
                THIS COULD HAVE BEEN CAUSED BY PERSONAL VIEWING BY YOU"
        )

        video_page.add_english_subtitles()

        self.assertTrue(
            video_page.has_subtitles(),
            msg="add_subitles_from_no_subtitles_state failed to add (english) subtitles "
        )

        # CLEANUP- Netflix's Akira player remembers subtitles from previous viewings.
        video_page.remove_subtitles()

    def test_remove_subtitles_from_subtitle_state(self):
        """From a state with subtitles, remove subtitles."""
        video_page = pagemodels.videopage.VideoPage(self.driver)

        if not video_page.has_subtitles():
            video_page.add_english_subtitles()

        self.assertTrue(
            video_page.has_subtitles(),
            msg="remove_subtitles_from_subtitle_state was not a subtitle state from start"
        )

        video_page.remove_subtitles()

        self.assertFalse(
            video_page.has_subtitles(),
            msg="remove_subtitles_from_subtitle_state failed to remove subtitles"
        )

    def test_change_audio_to_spanish_from_english_state(self):
        """From english audio state, change to spanish audio."""
        video_page = pagemodels.videopage.VideoPage(self.driver)
        # DEFAULT STATE IS ALWAYS ENGLISH
        current_audio = video_page.get_current_audio()

        self.assertIn(
            'nglish',
            current_audio,
            msg="test_change_audio_to_spanish_from_english_state wasnt an english state"
        )

        video_page.change_audio_to_spanish()

        new_audio = video_page.get_current_audio()
        self.assertIn(
            'anish',
            new_audio,
            msg="test_change_audio_to_spanish_from_english_state failed to change audio spanish"
        )

        # CLEANUP
        video_page.change_audio_to_english_original()

    def test_change_audio_to_english_from_spanish_state(self):
        """From spanish audio state, change to english audio."""
        # NOTE- english original not english. Doesnt work on non english original shows
        video_page = pagemodels.videopage.VideoPage(self.driver)

        # DEFAULT STATE IS ALWAYS ENGLISH
        video_page.change_audio_to_spanish()

        current_audio = video_page.get_current_audio()
        self.assertIn(
            'anish',
            current_audio,
            msg="test_change_audio_to_english_from_spanish_state wasnt a Spanish state"
        )

        video_page.change_audio_to_english_original()

        new_audio = video_page.get_current_audio()
        self.assertIn(
            'nglish',
            new_audio,
            msg="test_change_audio_to_english_from_spanish_state failed to change audio English"
        )

    # SKIP FORWARD/BACKWARD TESTS
    def test_skip_forward_30_seconds(self):
        """Using the skip forwad button, skip forwad 30 seconds."""
        video_page = pagemodels.videopage.VideoPage(self.driver)

        current_time = video_page.get_remaining_time_in_seconds()

        video_page.skip_forward()
        video_page.skip_forward()
        video_page.skip_forward()

        new_time = video_page.get_remaining_time_in_seconds()

        # when paused, delta < 0.01, when not paused and good connection, delta < 5
        self.assertAlmostEqual(current_time + 30, new_time, delta=5)

    def test_skip_back_30_seconds(self):
        """Using the skip back button, skip back 30 seconds."""
        # skipping back at 0:00 will cause the test to fail even though the act of skipping
        # back three times will not fail
        video_page = pagemodels.videopage.VideoPage(self.driver)

        current_remaining_time = video_page.get_remaining_time_in_seconds()
        show_duration = video_page.get_show_duration_in_seconds()

        self.assertGreater(
            show_duration-current_remaining_time,
            35,
            msg="test_skip_back_30_seconds can't skip back when the video isnt even 30 seconds in"
        )

        video_page.skip_backward()
        video_page.skip_backward()
        video_page.skip_backward()

        new_remaining_time = video_page.get_remaining_time_in_seconds()
        # WHEN PAUSED, delta < 0.01, WHEN NOT PAUSED AND GOOD CONNECTION, delta < 5
        self.assertAlmostEqual(current_remaining_time-30, new_remaining_time, delta=5)

#     # TIME/DURATION TESTS
    def test_go_to_halfway_point(self):
        """Go to the halfway point in the show/movie using the duration slider."""
        video_page = pagemodels.videopage.VideoPage(self.driver)

        video_page.change_to_percentage_time(.5)

        show_duration = video_page.get_show_duration_in_seconds()

        current_remaining_time = video_page.get_remaining_time_in_seconds()
        # print(f" show duration is {show_duration}")
        # print(f"current time is {current_time}")

        self.assertAlmostEqual(show_duration/2, current_remaining_time, delta=10)
        # Largest observed delta is 6.5 seconds. Not sure what is causing this delta.
        # seems to be intermittent. Could be the off by a pixel again. BUG- low priority
        # Maybe it would be eliminated by making a .get_current_time_in_seconds function
        # instead of relying on .get_remaining_time_in_seconds()

    def test_restart_show(self):
        """Restart a show by setting the percentage_time to 0."""
        video_page = pagemodels.videopage.VideoPage(self.driver)

        video_page.change_to_percentage_time(0)

        current_remaining_time = video_page.get_remaining_time_in_seconds()
        show_duration = video_page.get_show_duration_in_seconds()

        self.assertAlmostEqual(current_remaining_time, show_duration, delta=5)

        # CLEANUP
        # HALFWAY POINT IS THE DEFAULT STATE
        video_page.change_to_percentage_time(.5)

    # EXIT PLAYER TESTS
    def test_exit_player(self):
        """Exit the player by clicking the built-in back arrow button."""
        video_page = pagemodels.videopage.VideoPage(self.driver)
        video_page.go_back_to_shows()

        self.assertNotIn('watch', self.driver.current_url)
        # when watching a show, the url structure is "https://www.netflix.com/watch/600230...""

    # TESTS THAT DIDNT MAKE THE FIRST CUT
    # # # # # GO TO CREDITS COMPLICATES THINGS
    # # # # # TODO- I NEED A  videopage FUCNTIONS TO "watch credits" to redisplay the scrubber
    # def test_go_to_credits(self):
    #     """ UNTESTED, DO NOT USE"""
    #     """ go to the .98  point in the show/movie USING THE SLIDER"""
    #     video_page = pagemodels.videopage.VideoPage(self.driver)

    #     video_page.change_to_percentage_time(.98)

    #     show_duration = video_page.get_show_duration_in_seconds()

    #     current_remaining_time = video_page.get_remaining_time_in_seconds()


if __name__ == "__main__":
    unittest.main()
