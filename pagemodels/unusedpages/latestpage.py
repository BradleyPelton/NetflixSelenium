

# for some reason, the latest tab on located on the header is a special page. 
# There other tabs, Home = /browse, TV Shows = /genre/83, Movies= /genre/34399, mylist=mylist
# BUT FOR SOME REASON, Latest is a special page, sort of like the home page 

# THE ROWS:
### New Movies
### Trending Now
### New TV Shows
### Coming This week
### Coming Next Week 

# Trending is already on the home page, The other 4 rows are unique

########################################################################################
########################################################################################
# THIS PAGE IS NOT CURRENTLY SUPPORTED. YOUR RESULTS MAY VARY
########################################################################################
########################################################################################


def main_recommendation_latest(driver) -> int:
    """ DUPLICATE FUCNTION FROM /homepage.py . Works just as well"""
    """returns the id for the show that is the primary "ad" seen on the top 
    of the home page. The first thing a user sees. Usually 4/5ths of the screen
    NETFLIX CALLS THIS THE MAIN BILLBOARD
    """
    # the main page doesnt display almost any of the information displayed
    # in the JAWBONE. I would rather not redirect to /title/80050063 to retrieve
    # all of this information, but it might be unavoidable
    # TODO- RETURN MORE INFORMATION THAN JUST THE ID

    more_info_button = driver.find_element_by_css_selector(
        'a[data-uia="play-button"] + a')
    # sibling to the play button. TODO- Maybe cleaner css?
    title_link = more_info_button.get_attribute('href')
    title_id = int(title_link.split("/")[-1])
    return(title_id)
