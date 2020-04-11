
import pickle 
import datetime
import test_loginpage


browser_settings = dict()

browser_settings['last_updated'] = datetime.date.today()




# LOG IN BEFORE PROCEEDING 

with open('pickledcookies.pkl','rb') as pickledcookies:
    browser_settings = pickle.load(pickledcookies)
    print(f"browser_settings was last updated on {browser_settings['last_updated']}")
    if browser_settings['last_updated'] != datetime.date.today():
        # we need to login and pass new cookies
        APIlogin.login(username, password)
        pickle.dump(browser_settings, pickledcookies)
    else:
        pass