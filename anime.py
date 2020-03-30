import time
from collections import defaultdict

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from login import driver, user_login
import secrets
import mylisttools
import showtools

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
time.sleep(3)
driver.get('https://Netflix.com/browse/my-list')
# driver.get('https://www.netflix.com/browse/genre/7424')

# change sort to a-z to force all shows to load
switch_to_grid_view_button = driver.find_element_by_css_selector('button.aro-grid-toggle')
switch_to_grid_view_button.click()

dropdown_sort = driver.find_element_by_css_selector('div.nfDropDown.widthRestricted.theme-aro')
dropdown_sort.click()

a_through_z_sort_option = driver.find_element_by_css_selector('div.sub-menu.theme-aro > ul > li:nth-child(3)')
a_through_z_sort_option.click()

current_sort_option = driver.find_element_by_css_selector('div.nfDropDown.widthRestricted.theme-aro > div')
print(f"Currently sourting by {current_sort_option.text}")

shows = driver.find_elements_by_css_selector('a[class="slider-refocus"]')

#FINISHED SCRIPT
#TODO- GENERALIZE ThiS TO GENRE_SCRAPE FUCNTION
# EVERYTHING BELOW WOULD JUST BE GENRE_SCRAPE(GENRE_ID=7424)   ### 7424=ANIME
anime_shows_dict = defaultdict(dict)
for show in shows:
    title = show.text
    anime_shows_dict[title] = {}  #add show title to 
    # OPEN JAWBONE
    show.click()
    # Let jawbone load
    time.sleep(3)
    #
    if showtools.show_has_saved_progress(driver, show, JAWBONE_OPEN=True):
        anime_shows_dict[[title]['progress'] = 'T'
    else:
        anime_shows_dict[[title]['progress'] = 'F'
    #
    if mylisttools.is_in_my_list(driver, show, JAWBONE_OPEN=True):
        anime_shows_dict[[title]['is_in_my_list'] = 'T'
    else:
        anime_shows_dict[title]['is_in_my_list'] = 'F'
    #
    #
    ###### TODO- SINCE SHOW DETAILS ARE NOT DISPLAYED FROM THE OVERVIEW TAB
    # BECAUSE THE MOVIE HAS PROGRESS SAVED, I NEED TO NAVIGATE TO DETAILS
    #  menu = driver.find_element_by_css_selector('.menu')
    # issue with clicking the details button
    #
    # RECORD CAST, GENRE, TAGS TODO- convert this to a function that takes in
    # show elements 
    meta_lists_element = driver.find_element_by_css_selector('div.meta-lists')
    nested_lists = meta_lists_element.find_elements_by_tag_name('p')
    if len(nested_lists) != 3:
        print(f"show {title} is missing a meta_list ")
        continue
    cast_element_list = nested_lists[0]
    genre_element_list = nested_lists[1]
    tags_element_list = nested_lists[2]
    #
    actors_elements = cast_element_list.find_elements_by_tag_name('a')
    actors = [element.text for element in actors_elements]
    #
    genre_elements = genre_element_list.find_elements_by_tag_name('a')
    genres = [element.text for element in genre_elements]
    #
    tags_elements = tags_element_list.find_elements_by_tag_name('a')
    tags = [element.text for element in tags_elements]
    #
    anime_shows_dict[title]['actors'] = actors
    anime_shows_dict[title]['genres'] = genres
    anime_shows_dict[title]['tags'] = tags
    #
    jawBone_close_button = driver.find_element_by_css_selector('button.close-button.icon-close')
    jawBone_close_button.click()
    time.sleep(3)



# WORKSPACE. EVERYTHING BELOW SHOULD BE COMMENTED OUT
# OR DELETED BEFORE PUBLISHING 

import time
from collections import defaultdict

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from login import driver, user_login
import secrets
import mylisttools
import showtools


user_login(secrets.bradleys_email,secrets.bradleys_password)
driver.get('https://Netflix.com/browse/my-list')
driver.get('https://www.netflix.com/browse/genre/452?so=az')
shows = driver.find_elements_by_css_selector('a[class="slider-refocus"]')

temp = shows[0]
