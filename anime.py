from collections import defaultdict

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from login import driver, user_login, wait
import secrets
import mylisttools
import showtools
import genrepagetools

# len(shows) has been returning 144. 144 total animes in genre 7424

# CURRENT SCRAPE:
# Show.title, Cast, Genre, Tag.
# TODO- Add to scrape: In progress, Has been rated, upvoted or downvoted,
# bool(in_my_list), bool(netflix_original)
# Maybe scraping description, TBD, 

# TODO- When a meta list is missing, none of the lists are added
# add logic that adds whichever lists are there
# e.g. if only cast and genre but not tag
# anime_shows_dict[key] = {cast: {...} , genre: {...}}
# for k , v in anime_shows_dict.items():
#     if not v:
#             print(k)


# login
user_login(secrets.bradleys_email,secrets.bradleys_password)
# driver.get('https://Netflix.com/browse/my-list')
driver.get('https://www.netflix.com/browse/genre/7424')

# change sort to a-z to force all shows to load
genrepagetools.switch_to_grid(driver)
genrepagetools.switch_to_alpha_sort(driver)
print(f"Currently sourting by {current_sort_option.text}")

genrepagetools.master_sweep(driver, 7424)


###############################################################################
# WORKSPACE. EVERYTHING BELOW SHOULD BE COMMENTED OUT
# OR DELETED BEFORE PUBLISHING 
###############################################################################

import time
from collections import defaultdict

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


from login import user_login
import secrets
import mylisttools
import showtools
import genrepagetools

user_login(secrets.bradleys_email,secrets.bradleys_password)

driver.get('https://www.netflix.com/browse/genre/7424')

# change sort to a-z to force all shows to load
genrepagetools.switch_to_grid(driver)
genrepagetools.switch_to_alpha_sort(driver)
current_sort_option = driver.find_element_by_css_selector('div.nfDropDown.widthRestricted.theme-aro > div')
print(f"Currently sourting by {current_sort_option.text}")
shows = driver.find_elements_by_css_selector('a[class="slider-refocus"]')
temp = shows[2]


# unrelated. messing around with actionchains
action = ActionChains(driver)
action.key_down(Keys.CONTROL).send_keys('f').key_up(Keys.CONTROL).perform()
# Apparently I have to action.reset_actions() ????

