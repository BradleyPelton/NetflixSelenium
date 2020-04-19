import pickle
import datetime

import browserconfig
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
#     r'C:\Users\mavri\Desktop\Projects\netflixselenium\tests\pickledcookies.pkl',
#     'wb'
# ) as pickledcookies:
#     pickle.dump(browser_settings, pickledcookies)
##########################################################################
##########################################################################
##########################################################################


# driver = browserconfig.driver_runner(
#     executable_path=browserconfig.driver_path,
#     options=browserconfig.current_options
# )

def pickled_login(driver):
    """ IF TODAYS COOKIES ARE STILL VALID, USE TODAYS COOKIES TO LOG IN.
    ELSE: LOGIN THE OLD FASHION WAY AND STORE COOKIES
    """
    with open(
        r'C:\Users\mavri\Desktop\Projects\netflixselenium\tests\pickledcookies.pkl',
        'rb'
    ) as pickledcookies:
        browser_settings = pickle.load(pickledcookies)

        driver.delete_all_cookies()  # precaution in case anything is stored before we start

        driver.get('https://netflix.com')

        if browser_settings['last_updated'] == datetime.date.today():
            # add all of the cookies from the previous login
            for cookie in browser_settings['stored_cookies']:
                driver.add_cookie({k: v for k, v in cookie.items() if k != 'expiry'})
            driver.refresh()
            # refreshing the login page, with valid cookies, sends a user to the home page
        else:
            login_page = pagemodels.loginpage.LoginPage(driver)
            login_page.user_login(
                secrets.MY_EMAIL, secrets.MY_PASSWORD
            )

            browser_settings = dict()
            browser_settings['last_updated'] = datetime.date.today()
            browser_settings['stored_cookies'] = driver.get_cookies()
            with open(
                r'C:\Users\mavri\Desktop\Projects\netflixselenium\tests\pickledcookies.pkl',
                'wb'
            ) as pickledcookies:
                pickle.dump(browser_settings, pickledcookies)

# with open(r'C:\Users\mavri\Desktop\Projects\netflixselenium\tests\pickledcookies.pkl', 'rb') as pickledcookies:
#     browser_settings = pickle.load(pickledcookies)

# for cookie in browser_settings['stored_cookies']:
#     driver.add_cookie({k: v for k,v in cookie.items() if k!= 'expiry'})
#     # Interesting that expiry had to be excluded
#     # print(cookie)
