from selenium import webdriver
import selenium.webdriver.chrome.options
import selenium.webdriver.firefox.options
import selenium.webdriver.edge.options

import secrets
# THIS IS A CONFIG FILE.


# UNCOMMENT THE BROWSER YOU WANT TO TEST WITH
# ONLY ONE BROWSER SHOULD BE UNCOMMENTED AT A TIME
#########################################################################
#########################################################################
#########################################################################
# CHOOSE A BROWSER TO TEST WITH
# current_browser = 'chrome'
# current_browser = 'firefox'
current_browser = 'edge'
# current_browser = 'safari'
# current_browser = 'opera'
#########################################################################
#########################################################################
#########################################################################

if current_browser == 'chrome':
    driver_path = secrets.chromedriver_path
    driver_runner = webdriver.Chrome
elif current_browser == 'firefox':
    driver_path = secrets.geckodriver_path
    driver_runner = webdriver.Firefox
    # BUG TODO- VIDEO WONT PLAY FOR FIREFOX. I've tried signing in, drm toggle on/off
elif current_browser == 'edge':
    driver_path = secrets.msedgedriver_path
    driver_runner = webdriver.Edge
    # TODO- NICE TO HAVE- squelch warnings in edge
elif current_browser == 'safari':
    pass
elif current_browser == 'opera':
    pass





########################################################################################
########################################################################################
# OPTIONS/ DESIRED CAPABILITIES
########################################################################################
########################################################################################
# ADD ANY OPTIONS YOU WANT USING THE SAME SYNTAX BELOW
# It is okay not to have any options and just pass Options() as a parameter to webdriver

# capabilities = DesiredCapabilities.CHROME.copy()

if current_browser == 'chrome':
    current_options = selenium.webdriver.chrome.options.Options()
    # current_options.add_argument('--headless')  # see .set_headless below for a more hip way
    # current_options.set_headless(headless=True)
    # current_options.add_argument('--disable-extensions')
    current_options.add_argument('--window-size=1920,1080')
    # current_options.add_argument('--disable-gpu')
    capabilities = current_options.to_capabilities()
elif current_browser == 'firefox':
    current_options = selenium.webdriver.firefox.options.Options()
    # current_options.add_argument("--headless")
    capabilities = current_options.to_capabilities()
elif current_browser == 'edge':
    current_options = selenium.webdriver.edge.options.Options()
    # current_options.add_argument("--headless")
    capabilities = current_options.to_capabilities()



# cls.driver = browserconfig.driver_runner(
#     executable_path=browserconfig.driver_path,
#     desired_capabilities=browerconfig.capabilities
# )
# tests.pickledlogin.pickled_login(driver)
