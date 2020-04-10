https://stackoverflow.com/questions/18421280/selenium-python-click-on-element-nothing-happensz
https://www.selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.action_chains.html
https://gist.github.com/dariodiaz/3104601
https://stackoverflow.com/questions/12159874/click-method-will-not-always-work
https://github.com/aslushnikov/getting-started-with-cdp/blob/master/README.md
https://www.selenium.dev/selenium/docs/api/py/webdriver_chrome/selenium.webdriver.chrome.webdriver.html
https://www.selenium.dev/documentation/en/webdriver/browser_manipulation/
https://www.selenium.dev/documentation/en/support_packages/working_with_cookies/
https://stackoverflow.com/questions/33225947/can-a-website-detect-when-you-are-using-selenium-with-chromedriver/41904453#41904453
https://stackoverflow.com/questions/53039551/selenium-webdriver-modifying-navigator-webdriver-flag-to-prevent-selenium-detec/53040904#53040904
https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.chrome.options
https://selenium-python.readthedocs.io/waits.html#explicit-waits

### TOPICS TO EXPLORE:
- ActionChains class
    - https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.action_chains
- Optimal explicit waits 
- https://en.wikipedia.org/wiki/Microsoft_UI_Automation
- Netflix uses a cool UIA ID of the form `data-uia="myListButton"`


action = ActionChains(driver)
action.key_down(Keys.CONTROL).key_down(Keys.F).key_up(Keys.CONTROL).perform()