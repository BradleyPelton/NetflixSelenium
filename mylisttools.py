import time

# TODO- remove time.sleeps, add selenium waits for element to be present

# TODO- are these really mylisttools or just showtools??? consolidate/combine?

def is_in_my_list(driver, show_element, JAWBONE_OPEN=False) -> bool:
    """ RETURNS TRUE IF SHOW IS ALREADY IN My-List, FALSE IF ELSE"""
    if JAWBONE_OPEN:
        print("jawbone is already open, proceeding forward")
    else:
        show_element.click()

    time.sleep(3)
    my_list_button = driver.find_element_by_css_selector(
        'a[data-uia="myListButton"]')

    if my_list_button.get_attribute('aria-label') == 'Remove from My List':
        return(True)
    else:
        return(False)
    # TODO- The jawbone is still open. Maybe it should be closed? TBD


def add_show_to_my_list(driver, show_element):
    time.sleep(3)
    show_element.click()  # Opens JAWBONE (REQUIRED)
    time.sleep(3)
    my_list_button = driver.find_element_by_css_selector(
        'a[data-uia="myListButton"]')

    if is_in_my_list(driver, show_element, JAWBONE_OPEN=True):
        print("SHOW IS ALREADY IN YOUR LIST, NOT EXECUTING add_show_to_my_list")
    else:
        print("attempting to add to my list")
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

