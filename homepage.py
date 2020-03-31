import time

# the homepage of netflix is netflix.com/browse
# After successful login, users are redirected to `netflix.com/browse`
# netflix.com is redirected to this home page as well `netflix.com/browse`

driver.get('https://netflix.com')


def main_recommendation(driver) -> int:
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


def get_recommended_genres(driver) -> list:
    """ TODO- BREAK THIS INTO MULTIPLE FUNCTIONS:
    NAMELY: TOP 10 US, TOP PICKS FOR BRADLEY, GENRES(THIS FUNCTION), ETC.
    """
    # ASSUMES DRIVER IS ALREADY AT THE HOME PAGE 

    # SCROLL TO THE BUTTOM OF THE HOME PAGE
    # 10 lazy loads by netflix. Have to scroll to the bottom, then more loads
    # repeat 10 times
    for i in range(10):
        driver.execute_script("window.scrollTo(0, 10000000)")
        print(i)
        time.sleep(1)

    # THIS IS GENRES AND "My List"
    genre_rows = driver.find_elements_by_css_selector('a.rowTitle')
    genres = [genre.text for genre in genre_rows]
    return(genres)
    # for row in rows:
    #     print(row.text)
    # #notably includes:
    # My List
    # Because you watched Cells at Work!
    # New Releases
    # #notably excludes:
    # Continue Watching for Bradley
    # Popular on netflix
    # Trending Now
    # Top 10 in the U.s. Today
    # Top Picks for Bradley
    # Because you added Goodfellas to your List

    # # this was an interesting idea, but the element that contains the title
    # # is the sibling before the id=row-37 element. We cant go backwards or up with css
    # for i in range(0,38):
    #     row = driver.find_element_by_css_selector('#row-'+str(i))