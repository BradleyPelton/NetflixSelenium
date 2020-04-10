import time

from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from pagemodels.basepage import BasePage

# SHOWTTOOLS IS NOT AN ACTUALY PAGE. IT IS, HOWEVER, A COLLECTION OF FUNCTIONS
# THAT ARE APPLICABLE TO 95% OF THE WEB APP. EVERY NON-VIDEOPAGE PAGE IS A COLLECTION OF
# THESE SHOW ELEMENTS. THUS, THEY ARE GETTING THEIR OWN ELEMENT PAGE

# NOTE- SHOW ELEMENTS ARE OFTEN RETURNED FROM ROW_OPERATIONS. SEE homepage.py IF YOU NEED TO
# GRAB A SHOW ELEMENT FROM A PAGE, SINCE EVERY SHOW ELEMENT APPEARS IN A ROW, GO THERE

# IMPORTANT NOTE
# JAWBONE IS THE EXPANDED MENU THAT APPEARS WHEN YOU CLICK ON A SHOW ELEMENT
# BOB-CARD/BOB-CONTAINER IS THE MINI MENU THAT APPEARS WHEN YOU HOVER OVER A SHOW ELEMENT

# ELEMENT PAGE(SEE ABOVE)
class ShowToolsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        #Locators
        self.PLAY_BUTTON = (By.CSS_SELECTOR, 'a[data-uia="play-button"] > span')
        self.MY_LIST_BUTTON = (By.CSS_SELECTOR, 'a[data-uia="myListButton"]')
        self.DURATION = (By.CSS_SELECTOR, 'span.duration')
        self.PROGRESS_SUMMARY = (By.CSS_SELECTOR, 'span.summary')
        self.AUDIO_DESCRIPTION_BADGE = (By.CSS_SELECTOR, 'span.audio-description-badge')
        self.MATURITY_RATING = (By.CSS_SELECTOR, 'span.maturity-rating > span.maturity-number')
        self.MATCH_SCORE = (By.CSS_SELECTOR, 'span.match-score')
        self.SYNOPSIS = (By.CSS_SELECTOR, 'div.synopsis')
        self.RELEASE_YEAR = (By.CSS_SELECTOR, 'span.year')
        self.CAST_LIST = (By.CSS_SELECTOR, 'div.meta-lists > p.cast.inline-list')
        self.GENRE_LIST = (By.CSS_SELECTOR, 'div.meta-lists > p.genres.inline-list')
        self.TAGS_LIST = (By.CSS_SELECTOR, 'div.meta-lists > p.tags.inline-list')
        self.ALREADY_UPVOTED_BIG_UPVOTE_BUTTON = (By.CSS_SELECTOR, 'a[aria-label="Already rated: thumbs up (click to remove rating)"]')
        self.ALREADY_DOWNVOTED_BIG_DOWNVOTE_BUTTON = (BY.CSS_SELECTOR, 'a[aria-label="Already rated: thumbs down (click to remove rating)"]')
        self.UPVOTE_BUTTON = (BY.CSS_SELECTOR, 'a[aria-label="Rate thumbs up"]')
        self.DOWNVOTE_BUTTON = (By.CSS_SELECTOR, 'a[aria-label="Rate thumbs down"]')
        # BOB LOCATORS
        self.BOB_PLAY_HITZONE = (By.CSS_SELECTOR, 'div.bob-play-hitzone')
        self.BOB_PLAY_BUTTON = (By.CSS_SELECTOR, 'div.bob-overview a[data-uia="play-button"]')
        self.BOB_JAWBONE_HITZONE = (By.CSS_SELECTOR, 'div.bob-overlay > a.bob-jaw-hitzone')
        self.BOB_ALREADY_UPVOTED_BUTTON = (By.CSS_SELECTOR, 'div.bob-actions-wrapper a[aria-label="Already rated: thumbs up (click to remove rating)"]')
        self.BOB_ALREADY_DOWNVOTED_BUTTON = (By.CSS_SELECTOR, 'div.bob-actions-wrapper a[aria-label="Already rated: thumbs down (click to remove rating)"]')
        self.BOB_UPVOTE_BUTTON = (By.CSS_SELECTOR, 'div.bob-actions-wrapper a[aria-label="Rate thumbs up"]')
        self.BOB_DOWNVOTE_BUTTON = (By.CSS_SELECTOR, 'div.bob-actions-wrapper a[aria-label="Rate thumbs down"]')
        self.BOB_MY_LIST_BUTTON = (By.CSS_SELECTOR, 'div.bob-actions-wrapper div[data-uia="myListButton"])')
        self.BOB_MY_LIST_STATUS = (By.CSS_SELECTOR, 'div.bob-actions-wrapper div[data-uia="myListButton"] > span')

        

    # JAWBONE FUCNTIONS
    # FOR SHOW PREVIEW FUNCTIONS(bob-container), SEE LINE 300+
    def open_jawbone_if_not_open(self, show_element, JAWBONE_OPEN):
        if not JAWBONE_OPEN:
            show_element.click()
            # WAIT UNTIL JAWBONE FINISHES LOADING
            wait = WebDriverWait(self.driver, 10)
            meta_lists_element = wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'div.meta-lists')))
            # TODO- Grab a better element to wait for here

    def is_in_my_list(self, show_element, JAWBONE_OPEN=False) -> bool:
        """ RETURNS TRUE IF SHOW IS ALREADY IN My-List, FALSE IF ELSE"""
        self.open_jawbone_if_not_open(show_element)

        my_list_button = self.driver.find_element(*self.MY_LIST_BUTTON)

        if my_list_button.get_attribute('aria-label') == 'Remove from My List':
            return True
        else:
            return False

    def add_show_to_my_list(self, show_element):
        self.open_jawbone_if_not_open()

        my_list_button = self.driver.find_element(*self.MY_LIST_BUTTON)

        if self.is_in_my_list(show_element, JAWBONE_OPEN=True):
            print("SHOW IS ALREADY IN YOUR LIST, NOT EXECUTING add_show_to_my_list")
        else:
            my_list_button.click()

    def remove_show_from_my_list(self, show_element):
        self.open_jawbone_if_not_open()

        my_list_button = self.driver.find_element(*self.MY_LIST_BUTTON)

        if self.is_in_my_list(show_element):
            my_list_button.click()
        else:
            print("SHOW ISNT IN YOUR LIST, NOT EXECUTING remove_show_from_my_list ")

    def play_show(self, show_element, JAWBONE_OPEN=False):
        """ Plays the show passed in as the parameter show_element """
        """ NOT TESTED, TODO- TEST """
        self.open_jawbone_if_not_open(show_element, JAWBONE_OPEN)

        play_button = self.driver.find_element(*self.PLAY_BUTTON)
        play_button.click()

    def is_show(self, show_element, JAWBONE_OPEN=False):
        """ not sure about needed this function or not. Leaving it here just in case"""
        pass

    def is_movie(self, show_element, JAWBONE_OPEN=False):
        """ movie is defined as not TV show. Everything is either a series episodes or a movie"""
        pass

    def get_duration(self, show_element, JAWBONE_OPEN=False) -> str:
        """ RETURNS STR, e.g.'1h 27m' FOR MOVIE, '1 Season' FOR SHOW """
        """ NOT TESTED- TODO- THIS SHOULD RECIEVE EXTRA ATTENTION TO TEST"""
        self.open_jawbone_if_not_open(show_element, JAWBONE_OPEN)

        duration = self.driver.find_element(*self.DURATION)
        return duration.text

    def show_has_saved_progress(self, show_element, JAWBONE_OPEN=False) -> bool:
        """ CHECK IF SHOW HAS SAVED PROGRESS, if so return True, else False"""
        self.open_jawbone_if_not_open(show_element, JAWBONE_OPEN)
        try:
            self.driver.find_element(*self.PROGRESS_SUMMARY)
            return True
        except NoSuchElementException:
            return False

    def get_show_saved_progress(self, show_element, JAWBONE_OPEN=False) -> str:
        self.open_jawbone_if_not_open(show_element, JAWBONE_OPEN)

        progress_summary = self.driver.find_element(*self.PROGRESS_SUMMARY)
        # print(f"show {show_element.text} has saved progress. {progress_summary.text} remain")
        return progress_summary.text

    def is_netflix_original(self, show_element, JAWBONE_OPEN=False) -> bool:
        """ return true if this show/movie is a netflix original, false if else"""
        # this one might be tricky. The only designation that a show is a Netflix
        # original seems to be the "N SERIES" logo that is added on to the series
        # logo(same image). Might have to compare against a list of confirmed
        # netflix originals or do some cool image analysis to see if the top left
        # pixel is the nextflix red
        pass

    def has_new_episodes(self, show_element, JAWBONE_OPEN=False) -> bool:
        """ IF A SHOW HAS the "NEW EPISODES" tile added to the image, return True
        false if else"""
        # Might be equally as hard to determine as _is_netflix_original
        # Netflix adds a "new episodes" box ontop of the the boxart
        # My only idea for runny this function is to improt some module
        # that can determine which pixels are supposed to be the netflix red
        pass

    def has_audio_description_available(self, show_element, JAWBONE_OPEN=False) -> bool:
        """ return True if the show has an audio description available, False if else"""
        self.open_jawbone_if_not_open(show_element, JAWBONE_OPEN)
        try:
            self.driver.find_element(*self.AUDIO_DESCRIPTION_BADGE)
            return True
        except NoSuchElementException:
            return False

    def get_maturity_rating(self, show_element, JAWBONE_OPEN=False) -> str:
        """ return the maturity rating for a show, E.G. 'PG', 'PG-13', 'TV-MA'"""
        """ UNTESTED, TODO- TEST"""
        self.open_jawbone_if_not_open(show_element, JAWBONE_OPEN)

        maturity_rating = self.driver.find_element(*self.MATURITY_RATING)
        return maturity_rating.text

    def get_show_match_percentage(self, show_element, JAWBONE_OPEN=False) -> str:
        """ returns the match percentage e.g. '99% Match' for Castlevania"""
        """ EDGE CASE: match percentage doesnt seem to always show"""
        """ NOT TESTED, TODO- TEST"""
        self.open_jawbone_if_not_open(show_element, JAWBONE_OPEN)

        match_score = self.driver.find_element(*self.MATCH_SCORE)
        # if no match score is displayed, driver will still find the match_score element,
        # but it will just return '' when match_score.text is called
        if match_score.text == '':
            return "No match score displayed"
        else:
            return match_score.text

    def get_synopsis(self, show_element, JAWBONE_OPEN=False) -> str:
        """NOT TESTED, TODO- TEST"""
        self.open_jawbone_if_not_open(show_element, JAWBONE_OPEN)

        synopsis = self.driver.find_element(*self.SYNOPSIS)
        return synopsis.text

    def get_release_date(self, show_element, JAWBONE_OPEN=False):
        """UNTESTED TODO-TEST"""
        self.open_jawbone_if_not_open(show_element, JAWBONE_OPEN)

        release_year = self.driver.find_element(*self.RELEASE_YEAR)
        return release_year.text

    def get_number_of_episodes(self):
        """TODO-not sure if this is going to be hard or not. """
        pass

    def get_actors_list(self, show_element, JAWBONE_OPEN=False) -> list:
        """ returns list of actors. TODO- IF actors arent available from JAWBONE,
        write the logic to navigate to the details tab of the jawbone, scrape the
        top 3 actors, and then return that.
        """
        self.open_jawbone_if_not_open(show_element, JAWBONE_OPEN)
        try:
            # not sure why I cant just add " > a" to the end of the css selector for cast _element
            cast_list = self.driver.find_element(*self.CAST_LIST)
            actors_elements = cast_list.find_elements_by_tag_name('a')
            actors = [element.text for element in actors_elements]
            return actors
            # TODO- CLEAN THIS UP
        except NoSuchElementException:
            return ["COULD NOT FIND ACTORS"]

    def get_genre_list(self, show_element, JAWBONE_OPEN=False) -> list:
        """ return a genre list if available. TODO- if not avaiable, scrape details"""
        self.open_jawbone_if_not_open(show_element, JAWBONE_OPEN)
        try:
            genre_list = self.driver.find_element(*self.GENRE_LIST)
            genres_a_tags = genre_list.find_elements_by_tag_name('a')
            genres = [element.text for element in genres_a_tags]
            return genres
            # TODO- CLEAN THIS UP. not sure why I couldnt add " > a" to genre_list css selectors
            # to just retrieve genres
        except NoSuchElementException:
            return ["COULD NOT FIND GENRES"]

    def get_tags_list(self, show_element, JAWBONE_OPEN=False) -> list:
        """ return a tags list if available. TODO- if not avaiable, scrape details"""
        self.open_jawbone_if_not_open(show_element, JAWBONE_OPEN)

        try:
            tags_list = self.driver.find_element(*self.TAGS_LIST)
            tags_a_elements = tags_list.find_elements_by_tag_name('a')
            tags = [element.text for element in tags_a_elements]
            return tags
            # TODO- CLEAN THIS UP. not sure why I couldnt add " > a" to genre_list css selectors
            # to just retrieve genres
        except NoSuchElementException:
            return ["COULD NOT FIND TAG"]

# UPVOTE/DOWNVOTE FUCNTIONS
    def is_upvoted(self, show_element, JAWBONE_OPEN=False):
        """ return bool if upvoted"""
        self.open_jawbone_if_not_open(show_element, JAWBONE_OPEN)
        try:
            self.driver.find_element(*self.ALREADY_UPVOTED_BIG_UPVOTE_BUTTON)
            return True
        except NoSuchElementException:
            return False

    def is_downvoted(self, show_element, JAWBONE_OPEN=False):
        """ return bool if upvoted"""
        self.open_jawbone_if_not_open(show_element, JAWBONE_OPEN)
        try:
            self.driver.find_element(*self.ALREADY_DOWNVOTED_BIG_DOWNVOTE_BUTTON)
            return True
        except NoSuchElementException:
            return False

    def upvote_show(self, show_element, JAWBONE_OPEN=False):
        """upvote if not already upvoted, pass if already upvoted
            weird edge cases: the upvote button disappears when a show is downvoted"""
        self.open_jawbone_if_not_open(show_element, JAWBONE_OPEN)
        if self.is_upvoted(show_element, JAWBONE_OPEN=True):
            print("already upvoted, upvote_show is not doing anything")
        elif self.is_downvoted(show_element, JAWBONE_OPEN=True):
            already_downvoted_big_downvoted_button = self.find_element(
                *self.ALREADY_DOWNVOTED_BIG_DOWNVOTE_BUTTON)
            already_downvoted_big_downvoted_button.click()
            upvote_button = self.driver.find_element(*self.UPVOTE_BUTTON)
            upvote_button.click()
        else:
            upvote_button = self.driver.find_element(*self.UPVOTE_BUTTON)
            upvote_button.click()

    def downvote_show(self, show_element, JAWBONE_OPEN=False):
        """weird edge cases: the upvote button disappears when a show is downvoted"""
        self.open_jawbone_if_not_open(show_element, JAWBONE_OPEN)
        if self.is_downvoted(show_element, JAWBONE_OPEN=True):
            print("already downvoted, downvote_show is not doing anything")
        elif self.is_upvoted(show_element, JAWBONE_OPEN=True):
            already_upvoted_big_upvote_button = self.driver.find_element(
                *self.ALREADY_UPVOTED_BIG_UPVOTE_BUTTON)
            already_upvoted_big_upvote_button.click()
            downvote_button = self.driver.find_element(*self.DOWNVOTE_BUTTON)
            downvote_button.click()
        else:
            downvote_button = self.driver.find_element(*self.DOWNVOTE_BUTTON)
            downvote_button.click()

    ##########################################################################################
    # -=-=-=-=-=-=-=-=-=-=-=-=- BOB CONTAINER FUNCTIONS =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=
    ##########################################################################################
    # NOT TO BE CONFUSED WITH THE JAWBONE FUCNTINOS ABOVE, THESE FUCNTIONS SOLELY WORK WITHIN
    # THE USE CASES WHEN A USER MOUSES OVER A SHOW ELEMENT, CAUSING A "BOB CONTAINER" to appear
    # NETFLIX CALLS THIS THE "BOB-CARD" "BOB OVERLAY" "BOB-JAW-HITZONE"

    def mouse_over_show_element(self, show_element):
        """ Mouse over a show_element to force the bob-container to open """
        action = ActionChains(self.driver)
        action.move_to_element(show_element).perform()
        # Wait for BOB CONTAINER to open
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located((self.BOB_PLAY_HITZONE)))

    def show_is_being_previewed(self):
        """ RETURN TRUE IF THERE IS A SHOW THAT IS CURRENTLY BEING MOUSED OVER. NOT TO BE CONFUSED
        WITH JAWBONE OPEN. EQUIVALENT TO is_bob_container_open() if it existed"""
        """NOTE- only one show can be previewed at a time so its valid just to search the entire
        dom"""
        try:
            self.driver.find_element(*self.BOB_PLAY_BUTTON)
            return True
        except NoSuchElementException:
            return False

    def mouse_over_show_if_not_moused_over(self, show_element):
        """ open the bob container of a show_element if its not already open. Mousing over it
        causes it to open """
        if self.show_is_being_previewed():
            pass
            # print("show is already being mousedover, mouse_over_show_if_not_moused_over not exe")
        else:
            self.mouse_over_show_element(show_element)

    def open_jawbone_from_show_preview(self, show_element):
        """ TODO- add logic to check if jawbone is already open."""
        self.mouse_over_show_if_not_moused_over(show_element)
        bob_jawbone_hitzone = self.driver.find_element(*self.BOB_JAWBONE_HITZONE)
        bob_jawbone_hitzone.click()

    def play_show_from_show_preview(self, show_element):
        """ play the show from the bob container by clicking in the center of the bob container"""
        self.mouse_over_show_if_not_moused_over(show_element)
        bob_play_hitzone = self.driver.find_element(*self.BOB_PLAY_HITZONE)
        bob_play_hitzone.click()

    # BOB UPVOTE/DOWNVOTE FUCNTIONS
    def show_is_upvoted_from_show_preview(self, show_element):
        """ return true if the show is upvoted AS SEEN FROM THE BOB CONTAINER, False if else"""
        self.mouse_over_show_if_not_moused_over(show_element)
        try:
            self.driver.find_element(*self.BOB_ALREADY_UPVOTED_BUTTON)
            return True
        except NoSuchElementException:
            return False

    def show_is_downvoted_from_show_preview(self, show_element):
        """ return true if the show is downvoted AS SEEN FROM THE BOB CONTAINER, False if else """
        self.mouse_over_show_if_not_moused_over(show_element)
        try:
            self.driver.find_element(*self.BOB_ALREADY_DOWNVOTED_BUTTON)
            return True
        except NoSuchElementException:
            return False

    def upvote_from_show_preview(self, show_element):
        """ upvote from preview if not upvoted, else do nothing"""
        self.mouse_over_show_if_not_moused_over(show_element)
        if self.show_is_upvoted_from_show_preview(show_element):
            print("show is already upvoted, upvote_from_show_preview not executing")
        elif self.show_is_upvoted_from_show_preview(show_element):
            bob_already_upvoted_button = self.driver.find_element(*self.BOB_ALREADY_UPVOTED_BUTTON)
            bob_already_upvoted_button.click()
            # HAVE TO WAIT FOR DOWNVOTE UNCLICK TO PROCESS AND FOR THE UPVOTE BUTTON TO APPEAR
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.visibility_of_element_located(self.BOB_UPVOTE_BUTTON))
            bob_upvote_button = self.driver.find_element(self.BOB_UPVOTE_BUTTON)
            bob_upvote_button.click()
        else:
            bob_upvote_button = self.driver.find_element(self.BOB_UPVOTE_BUTTON)
            bob_upvote_button.click()

    def downvote_from_show_preview(self, show_element):
        """ downvote from preview if not downvoted, else do nothing"""
        self.mouse_over_show_if_not_moused_over(show_element)
        if self.show_is_downvoted_from_show_preview(show_element):
            print("show is already downvoted, downvote_from_show_preview not executing")
        elif self.show_is_upvoted_from_show_preview(show_element):
            bob_already_upvoted_button = self.driver.find_element(self.BOB_ALREADY_UPVOTED_BUTTON)
            bob_already_upvoted_button.click()
            # HAVE TO WAIT FOR UPVOTE UNCLICK TO PROCESS AND FOR THE DOWNVOTE BUTTON TO APPEAR
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.visibility_of_element_located(self.BOB_DOWNVOTE_BUTTON))
            bob_downvote_button = self.driver.find_element(*self.BOB_DOWNVOTE_BUTTON)
            bob_downvote_button.click()
        else:
            bob_downvote_button = self.driver.find_element(*self.BOB_DOWNVOTE_BUTTON)
            bob_downvote_button.click()

    # BOB MY-LIST FUCNTIONS
    def show_is_in_my_list_from_show_preview(self, show_element):
        """ """
        self.mouse_over_show_if_not_moused_over(show_element)
        bob_my_list_button = self.driver.find_element(*self.BOB_MY_LIST_BUTTON)
        # I cant find another way to determine if the my list button is checked or not
        # The dom is surprisingly not helpful here. There is no is_checked attribute hidden in
        # an aria tag or anything. I'm going to have to brute force it by mousing over the my_list
        # _button and seeing what the text popup says
        # TODO- CLEAN THIS UP
        action = ActionChains(self.driver)
        action.move_to_element(bob_my_list_button).perform()
        status = self.driver.find_element_by_css_selector(*self.BOB_MY_LIST_STATUS)
        print(f"show status text is {status.text}")
        if status.text == 'Remove from My List':
            return True
        else:
            return False

    def add_show_to_my_list_from_show_preview(self, show_element):
        """ add show to my list using the bob container. If show already in my list, do nothing"""
        self.mouse_over_show_if_not_moused_over(show_element)
        if self.show_is_in_my_list_from_show_preview(show_element):
            print("show already in my list, add_show_to_my_list_from_show_preview not executing")
        else:
            bob_my_list_button = self.driver.find_element(*self.BOB_MY_LIST_BUTTON)
            bob_my_list_button.click()

    def remove_show_from_my_list_from_show_preview(self, show_element):
        """ """
        self.mouse_over_show_if_not_moused_over(show_element)
        if not self.show_is_in_my_list_from_show_preview(show_element):
            print("show isnt in mylistalready, remove_show_from_my_list_from_show_preview not exe")
        else:
            bob_my_list_button = self.driver.find_element(*self.BOB_MY_LIST_BUTTON)
            bob_my_list_button.click()
