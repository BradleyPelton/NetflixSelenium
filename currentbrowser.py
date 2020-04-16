import secrets

# THIS IS A CONFIG FILE.


# UNCOMMENT THE BROWSER YOU WANT TO TEST WITH
# ONLY ONE BROWSER SHOULD BE UNCOMMENTED AT A TIME
#########################################################################
#########################################################################
#########################################################################
current_browser = 'chrome'
# current_browser = 'firefox'
# current_browser = 'safari'
# current_browser = 'edge'
# current_browser = 'opera'
#########################################################################
#########################################################################
#########################################################################

if current_browser == 'chrome':
    driver_path = secrets.chromedriver_path
elif current_browser == 'firefox':
    driver_path = secrets.geckodriver_path
elif current_browser == 'edge':
    pass
elif current_browser == 'safari':
    pass
elif current_browser == 'opera':
    pass

# I need to pass in the webdriver.Chrome() function somehow
# maybe pack them into a tuple and unpack them at the page?
# I can't just set the path and driver here 