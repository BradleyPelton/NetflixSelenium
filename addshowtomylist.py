



shows = driver.find_elements_by_css_selector('a[class="slider-refocus"]')
for show in shows:
    if show.text == 'Cells at Work!':
        temp = show

# TODO- CREATE A FUNCTION THAT TAKES IN A SHOW ELEMENT AND PERFORMS THE FOLLOWING:

# JAWBONE NEEDS TO BE OPENED
my_list_button = driver.find_element_by_css_selector('a[data-uia="myListButton"]')
my_list_button.click()
#
if my_list_button.get_attribute('aria-label') == 'Remove from My List':
    print("SHOW IS ALREADY IN YOUR LIST")
else:
    my_list_button.click()





