from login import driver, user_login
import time
from collections import defaultdict
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException

time.sleep(3)
driver.get('https://www.netflix.com/browse/my-list')
time.sleep(3)

shows = driver.find_elements_by_css_selector('a[class="slider-refocus"]')

my_shows_dict = defaultdict(dict)
for show in shows:
    my_shows_dict[show.text] = {}
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
    except NoSuchElementException:
        pass
        # reword this god awful statement 
    #
    if len(nested_lists) != 3:
        print(f"show {show.text} is missing a meta_list such as cast")
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
    my_shows_dict[show.text]['actors'] = actors
    my_shows_dict[show.text]['genres'] = genres
    my_shows_dict[show.text]['tags'] = tags
    #
    jawBone_close_button = driver.find_element_by_css_selector('button.close-button.icon-close')
    time.sleep(3)





print(my_shows_dict)

