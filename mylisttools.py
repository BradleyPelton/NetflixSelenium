import time

# TODO- remove time.sleeps, add selenium waits for element to be present



# TODO- THERE IS A BUG HERE NOTE TODO NOTE 
# test adding a show to my list that is already in my list
# I believe the problem is from is_in_my_list




def is_in_my_list(driver, show_element) -> bool:
    """ RETURNS TRUE IF SHOW IS ALREADY IN My-List, FALSE IF ELSE"""
    show_element.click()  # Opens Jawbone (REQUIRED)
    time.sleep(3)
    my_list_button = driver.find_element_by_css_selector(
        'a[data-uia="myListButton"]')

    if my_list_button.get_attribute('aria-label') == 'Remove from My List':
        return(True)
    else:
        return(False)
    # TODO- The jawbone is still open. Maybe it should be closed? TBD


def add_show_to_my_list(driver, show_element):
    show_element.click()  # Opens JAWBONE (REQUIRED)
    time.sleep(3)
    my_list_button = driver.find_element_by_css_selector(
        'a[data-uia="myListButton"]')

    if is_in_my_list(driver, show_element):
        print("SHOW IS ALREADY IN YOUR LIST, NOT EXECUTING add_show_to_my_list")
    else:
        my_list_button.click()


def remove_show_from_my_list(driver, show_element):
    show_element.click()  # Opens JAWBONE (REQUIRED)
    time.sleep(3)
    my_list_button = driver.find_element_by_css_selector(
        'a[data-uia="myListButton"]')

    if is_in_my_list(driver, show_element):
        my_list_button.click()
    else:
        print("SHOW ISNT IN YOUR LIST, NOT EXECUTING remove_show_from_my_list ")
