### MOVIES AND SHOWS HAVE HIDDEN GENRES AND PUBLIC GENRES
### A PUBLIC GENRE IS SOMETHING LIKE "ROMANCE", "ACTION", "HORROR"
### A HIDDEN GENRE IS ASSIGNED BY NETFLIX AND DISPLAYED IN THE URL
### E.G https://www.netflix.com/browse/genre/83 FOR "Tv Shows"

# TODO- There are three other sort methods: Suggested for you, Z-A, Year Released
# CREATE FUCNTIONS FOR EACH OF THESE

def switch_to_grid(driver):
    """
    switch from the default row display( that scroll right to display more)
    to the grid view pattern
    by clicking the grid pattern button
    """
    switch_to_grid_view_button = driver.find_element_by_css_selector('button.aro-grid-toggle')
    switch_to_grid_view_button.click()

def switch_to_alpha_sort(driver):
    """
    click the dropdown that allows user to change the sort method
    change the sort method to alpha
    """
    dropdown_sort = driver.find_element_by_css_selector('div.nfDropDown.widthRestricted.theme-aro')
    dropdown_sort.click()

    a_through_z_sort_option = driver.find_element_by_css_selector('div.sub-menu.theme-aro > ul > li:nth-child(3)')
    a_through_z_sort_option.click()

# current_sort_option = driver.find_element_by_css_selector('div.nfDropDown.widthRestricted.theme-aro > div')
# print(f"Currently sourting by {current_sort_option.text}")
