
########################################################################################
########################################################################################
# THIS PAGE IS NOT CURRENTLY SUPPORTED. YOUR RESULTS MAY VARY
########################################################################################
########################################################################################


def play_random_show():
    """ 
    ASSUMES USER ALREADY LOGGED IN. PLAYS A RANDOM SHOW
    FROM THE USER'S 'MY-LIST' LIST.
    """
    # REMOVED A sleep here, refactor
    driver.get('https://www.netflix.com/browse/my-list')

    shows = driver.find_elements_by_css_selector('a[class="slider-refocus"]')

    random_index = random.randint(0,len(shows))
    random_show = shows[random_index]  # chooses the ith show where I random
    random_show.click()

    play_button = driver.find_element_by_css_selector('a[data-uia="play-button"] > span')
    play_button.click()