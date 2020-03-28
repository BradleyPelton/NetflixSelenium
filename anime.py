from login import driver
import time
from collections import defaultdict
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException

time.sleep(3)
driver.get('https://www.netflix.com/browse/genre/7424')

switch_to_grid_view_button = driver.find_element_by_css_selector('button.aro-grid-toggle')
switch_to_grid_view_button.click()

dropdown_sort = driver.find_element_by_css_selector('div.nfDropDown.widthRestricted.theme-aro')
dropdown_sort.click()

a_through_z_sort_option = driver.find_element_by_css_selector('div.sub-menu.theme-aro > ul > li:nth-child(3)')
a_through_z_sort_option.click()

current_sort_option = driver.find_element_by_css_selector('div.nfDropDown.widthRestricted.theme-aro > div')
print(f"Currently sourting by {current_sort_option.text}")

shows = driver.find_elements_by_css_selector('a[class="slider-refocus"]')

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
anime_shows_dict = defaultdict(dict)
for show in shows:
    anime_shows_dict[show.text] = {}
    show.click()
    # 
    time.sleep(3)
    meta_lists_element = driver.find_element_by_css_selector('div.meta-lists')
    nested_lists = meta_lists_element.find_elements_by_tag_name('p')
    #
        # if len(nested_lists) != 3:
        #     print(f"show {show.text} doesnt have all three meta_list types")
        #     continue
    try:
        progress_summary = driver.find_element_by_css_selector('span.summary')
        print(f"show {show.text} has saved progress. {progress_summary.text} remain")
        a = driver.find_element_by_id('tab-ShowDetails')
        ###### TODO- SINCE SHOW DETAILS ARE NOT DISPLAYED FROM THE OVERVIEW TAB
        # BECAUSE THE MOVIE HAS PROGRESS SAVED, I NEED TO NAVIGATE TO DETAILS
        #  menu = driver.find_element_by_css_selector('.menu')
        # issue with clicking the details button
        continue
        # print('continue')
    except NoSuchElementException:
        pass
        # reword this god awful statement 
        #
    if len(nested_lists) != 3:
        print(f"show {show.text} is missing a meta_list ")
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
    anime_shows_dict[show.text]['actors'] = actors
    anime_shows_dict[show.text]['genres'] = genres
    anime_shows_dict[show.text]['tags'] = tags
    #
    jawBone_close_button = driver.find_element_by_css_selector('button.close-button.icon-close')
    jawBone_close_button.click()
    time.sleep(3)





print(anime_shows_dict)