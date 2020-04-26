# NetflixSelenium

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


An automated test suite to test the core functionality of https://netflix.com , as well as
add additional functionality for users(video tools, random show picker, etc.). Key features include:
- Optimized for speed(no time.sleep() or implicit waits anywhere)
- POM design to minimize maintenance costs(in time)
- Elegant report generation with unittest/xmlrunner

## Quick Guide
- "I HAVE NO IDEA WHAT I'M LOOKING AT." Watch [gif of test execution](https://gyazo.com/7c703e6bba5af706849052df65772089), then
checkout [VideoPage tests](https://github.com/BradleyPelton/NetflixSelenium/blob/master/tests/test_videopage.py), it contains very straightforward tests(mute, pause, add subtitles, etc.).
- This test suite is organized in a Page-Object-Model(POM) design pattern. TLDR: tests contain the 
test logic (asserts, etc.), and Page objects [pagemodels](https://github.com/BradleyPelton/NetflixSelenium/tree/master/pagemodels) hold the logic for interacting with the page (e.g. press_play_buttonn).
- The POM design pattern is most the verbose(and the most complex) to write, but is the easiest to 
maintain in terms of both speed and complexity. See [selenium.dev/POM](https://www.selenium.dev/documentation/en/guidelines_and_recommendations/page_object_models/)

## Examples/Videos
- Watch VIDEO TESTS - gyazo sped up the [original video](https://gyazo.com/7c703e6bba5af706849052df65772089)
![video alt](https://i.gyazo.com/7c703e6bba5af706849052df65772089.gif)
- Watch HOME PAGE TESTS https://gyazo.com/8c9e75c1412c7e13e32b0b4bc14a5677
- Watch HEADER TOOLS TESTS https://gyazo.com/b20fd223076bf34c1f2c9b94a4f1fe0a
- Watch LOGIN TESTS https://gyazo.com/dd49e25639ec1b5c6fcac0ab5251fc4e

# Getting Started

## Setup
### Prerequisites 
- See `requirements.txt` for the simple requirements.
- Choose a browser/webdriver of your choice (see [selenium.dev/webdrivers](https://www.selenium.dev/documentation/en/webdriver/driver_requirements/#quick-reference)) I'm currently using:
    - Google Chrome version 81.0.4044.92, ChromeDriver version 81.0.4044.69
    - Firefox version v75.0, geckodriver-v0.26.0-win64
    - Edge version 81.0.416.53, msedgedriver version: 81.0.409.0

## Constants/Secrets
- You need to create a `secrets.py` file in the root directory that will hold all of your 
credentials and paths. In `secrets.py` set the following constants as strings `MY_EMAIL, MY_PASSWORD, MY_CHOMEDRIVER_PATH, MY_GECKODRIVER_PATH, MY_MSEDGEDRIVER_PATH, URL_OF_VIDEO_TO_TEST`

## Running the tests
Tests are executed using the standard unittest framework commands(or xmlrunner for reports)
- To execute all tests `$ python -m xmlrunner discover -o xmltestresults`
- To execute a specific test module `$ python -m xmlrunner tests/test_headerpage.py -o xmltestresults`


### DEAR NETFLIX DEVS:
As fun as it was to automate your web app, please reopen the public API! I would love to be able to
sort my shows by more than one category at a time, among other things, without having to build an 
entire project to do so.  I know there are drawbacks to adding more complicated features, but 
reintroducing the public API would be an awesome alternative.

Please kindly email me if you have any questions or concerns bradleypelton@gmail.com

## Acknowledgements
- First and foremost to Netflix for creating a beautiful UI. The UI is optimized for screen-readers
which also makes it heaven for locating elements. Almost every element has a human-readable data-uia
- I lay no claim to the underlying software of Netflix's web app. 
- Shoutout to the helpful devs on the Selenium Slack/IRC channel, see [slack.com/selenium](https://seleniumhq.slack.com/join/shared_invite/enQtODAwOTUzOTM5OTEwLTZjZjgzN2ExOTBmZGE0NjkwYzA2Nzc0MjczMGYwYjdiNGQ5YjI0ZjdjYjFhMjVlMjFkZWJmNDYyMmU1OTYyM2Y)
