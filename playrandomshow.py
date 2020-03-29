from login import driver, user_login
import secrets
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import random 


# TODO- feature idea- User could desire a show in my-list that has
# a certain genre, or exclude a certain genre, include/exclude certain tag,
# has a specific actor.

# Fully functional. Additional features could make this more interesting
def play_random_show():
    """ 
    ASSUMES USER ALREADY LOGGED IN. PLAYS A RANDOM SHOW
    FROM THE USER'S 'MY-LIST' LIST.
    """
    time.sleep(3)
    driver.get('https://www.netflix.com/browse/my-list')

    shows = driver.find_elements_by_css_selector('a[class="slider-refocus"]')

    random_index = random.randint(0,len(shows))
    random_show = shows[random_index]  # chooses the ith show where I random
    random_show.click()

    play_button = driver.find_element_by_css_selector('a[data-uia="play-button"] > span')
    play_button.click()


if __name__ == "__main__":
    user_login(secrets.bradleys_email, secrets.bradleys_password)
    play_random_show()
