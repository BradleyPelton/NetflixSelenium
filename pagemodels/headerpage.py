


# TODO- HEADER IS TO GET ITS OWN PAGE EVEN THOUGH ITS NOT A PAGE
###########################################################################################
###########################################################################################
###########################################################################################
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= HEADER FUNCTIONS =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#  THE FOLLOWING FUNCTIONS ARE NOT SPECIFIC TO THE HOMEPAGE. ALL PAGES HAVE ACCESS TO THIS HEADER
# AND THUS ALL OF THESE FUNCIONS. TODO- DECIDE WHETHER THESE FUNCIONS SHOULD HAVE THEIR OWN PAGE
###########################################################################################
###########################################################################################
###########################################################################################


def logout(driver):
    """ self explantory, tested"""
    account_dropdown_button = driver.find_element_by_css_selector('div.account-dropdown-button')
    account_dropdown_button.click()
    # time.sleep(3)
    dropdown_options = driver.find_elements_by_css_selector('ul.account-links.sub-menu-list > li')

    logout_button = dropdown_options[2]
    logout_button.click()


def navigate_to_manage_profile(driver):
    """ navigate to the manage profiles page, https://www.netflix.com/profiles/manage, by clicking
    on the manage profiles button from the account dropdown from the header
    """
    """ NOTE- while these functions contribute to completeness by testing individual buttons, it
    is much more important to test key features in the first version of the automation suite"""
    account_dropdown_button = driver.find_element_by_css_selector('div.account-dropdown-button')
    account_dropdown_button.click()
    #
    manage_profiles_button = driver.find_element_by_css_selector('a[aria-label="Manage Profiles"]')
    manage_profiles_button.click()


def clear_notifications(driver):
    """ CLEAR NOTIFICATIONS BY OPENING THE NOTIFICATIONS DROPDOWN AND THEN CLOSING IT"""
    """ TODO- NEED NOTIFIATIONS TO APPEAR AGAIN TO TEST. TODO"""
    notifications_menu_button = driver.find_element_by_css_selector(
        'button[aria-label="Notifications"]'
    )
    notifications_menu_button.click()
    notifications_menu_button.click()


def click_top_notification(driver):
    """ self-explanatory. Works from every non-video page"""
    notifications_menu_button = driver.find_element_by_css_selector(
        'button[aria-label="Notifications"]'
    )
    notifications_menu_button.click()
    #
    notifications_container = driver.find_element_by_css_selector('ul.notifications-container')
    notifications = notifications_container.find_elements_by_css_selector('div > li.notification')
    #
    top_notification = notifications[0]
    top_notification.click()


def search_field_is_open(driver) -> bool:
    """ return True if the search field is open, False if else"""
    try:
        driver.find_element_by_css_selector('input[data-uia="search-box-input"]')
        return(True)
    except NoSuchElementException:
        return(False)


def clear_search(driver):
    """ search field is non-empty IFF it is open. Thus we dont have to open the search field
     here"""
    search_field = driver.find_element_by_css_selector('input[data-uia="search-box-input"]')
    search_field.clear()


def search(driver, search_term: str):
    """ uses the search bar in the header to search for search_term"""
    """ TODO- This is a exactly what a serach is in theory, but in practice, Netflix handles things
    a little differently. Notice when searching things manually, the netflix app actually searches
    after EVERY SINGLE key press. Thus if we were to search for "Top Gun" manually, the observer
    will notice that 7 DIFFERENT page results are displayed in the results (len("Top Gun")). This
    is the fundamental difference between automation testing and automating user behavior. We need
    to actually mimic user behavior. In this case the 2 differ because Selenium.send_keys() sends
    all of the keys at the same time. TODO- THIS IS GOOD THEORY. GOOD DISCUSSION. READDD MEEEE"""
    if search_field_is_open(driver):
        clear_search(driver)
    else:
        # TODO- Turn open_seach_field into a function??? Seems a little verbose
        search_button = driver.find_element_by_css_selector('button.searchTab')
        search_button.click()
    search_field = driver.find_element_by_css_selector('input[data-uia="search-box-input"]')
    search_field.send_keys(search_term)


# def click_refer_button(driver):
#     """ waste of time. adding it here just for completeness"""
#     pass
