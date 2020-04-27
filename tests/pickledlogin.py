import pickle
import datetime

# import browserconfig
import secrets
import pagemodels.loginpage

##########################################################################
##########################################################################
##########################################################################
# CLEAR COOKIES\ HARD RESET \ accidentally deleted pickledcookies.pkl
# Delete the cookies by placing placeholder values in the browser_settings dict
# browser_settings = dict()
# browser_settings['last_updated'] = datetime.date(1980,1,1)
# browser_settings['stored_cookies'] = 1234567890
# with open(
#     r'tests\pickledcookies.pkl',
#     'wb'
# ) as pickledcookies:
#     pickle.dump(browser_settings, pickledcookies)
##########################################################################
##########################################################################
##########################################################################

def pickled_login(driver):
    """If stored cookies(in pickledcookies.pkl) are still valid (less than 24 hours old), use them
    to bipass logging in. Else, log in from https://netflix.com/login and save the newly created
    cookies.
    """
    with open(r'tests\pickledcookies.pkl', 'rb') as pickledcookies:
        browser_settings = pickle.load(pickledcookies)

        driver.delete_all_cookies()  # Precaution in case anything is stored before we start.

        driver.get('https://netflix.com/login')

        if browser_settings['last_updated'] == datetime.date.today():
            # Add all of the cookies from the previous login.
            for cookie in browser_settings['stored_cookies']:
                driver.add_cookie({k: v for k, v in cookie.items() if k != 'expiry'})
            driver.refresh()
            # Refreshing the login page, with valid cookies, sends a user to the home page.
        else:
            login_page = pagemodels.loginpage.LoginPage(driver)
            login_page.user_login(
                secrets.MY_EMAIL, secrets.MY_PASSWORD
            )

            browser_settings = dict()
            browser_settings['last_updated'] = datetime.date.today()
            browser_settings['stored_cookies'] = driver.get_cookies()
            with open(r'tests\pickledcookies.pkl', 'wb') as pickledcookies:
                pickle.dump(browser_settings, pickledcookies)

# Print current cookies
# with open(
#     r'tests\pickledcookies.pkl',
#     'rb'
# ) as pickledcookies:
    # browser_settings = pickle.load(pickledcookies)
    # print(browser_settings)

# Manually load the cookies
# for cookie in browser_settings['stored_cookies']:
#     driver.add_cookie({k: v for k,v in cookie.items() if k!= 'expiry'})
#     # Interesting that expiry had to be excluded
#     # print(cookie)
