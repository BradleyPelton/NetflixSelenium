# NetflixSelenium
An automated test suite(Selenium) to test the core functionality of https://netflix.com , as well as
add more functionality for users(e.g. advanced searching)

## Quick Guide
- "I HAVE NO IDEA WHAT IM LOOKING AT." Watch [gif of test execution](https://gyazo.com/37be44a9993676c4161adff157960e45) then
checkout [VideoPage tests](https://github.com/BradleyPelton/NetflixSelenium/blob/master/tests/test_videopage.py), it contains very straightforward tests(mute, pause, add subtitles, etc.).
- This test suite is organized in a Page-Object-Model(POM) design pattern. TLDR: tests contain the 
test logic (asserts, etc.), and Page objects [pagemodels](https://github.com/BradleyPelton/NetflixSelenium/tree/master/pagemodels) hold the logic for interacting with the page (click 'x' button, etc.).
- The POM design pattern is most the verbose(and the most complex) to write, but is the easiest to 
maintain in both speed and complexity. See [selenium.dev/POM](https://www.selenium.dev/documentation/en/guidelines_and_recommendations/page_object_models/)

## Examples/Videos
- Watch VIDEO TESTS https://gyazo.com/37be44a9993676c4161adff157960e45
- Watch HOME PAGE TESTS https://gyazo.com/6821682827f79a47ce16e66c34ce2fbb (TODO-REFILM)
- Watch HEADER TOOLS TESTS https://gyazo.com/b20fd223076bf34c1f2c9b94a4f1fe0a 

# Getting Started

## Setup
### Prerequsites
- You need selenium first and foremost `pip install selenium`
- Choose a browser and webdriver of your choice (see [selenium.dev/webdrivers](https://www.selenium.dev/documentation/en/webdriver/driver_requirements/#quick-reference)) I'm currently using:
    - Google Chrome version 81.0.4044.92, ChromeDriver version 81.0.4044.69
    - Firefox version v75.0, geckodriver-v0.26.0-win64
    - Edge version 81.0.416.53, msedgedriver version: 81.0.409.0

## Running the tests
Tests are executed using the standard unittest framework commands
- To execute all tests `python -m unittest discover .`
- To execute a specific test module `python -m unittest -v tests/test_videopage.py`


### DEAR NETFLIX DEVS:
The purpose of this repo is to provide advance searching to users, an area in which your current
app falls short unfortunately. A perfect example is sorting a category by additional characteristics
(e.g. sorting Action movies by tag='Exciting'). In your current app, a user can sort movies by tag 
or sort by genre, but not sort genre by tag.

Or you could always reopen the public API! 

Please kindly email me if you have any questions or concerns bradleypelton@gmail.com

## Acknowledgements
- First and foremost to Netflix for creating a beautiful UI. The UI is opitimized for screen-readers
which also makes it heaven for locating elements. Almost every element has a human-readable data-uia
- Shoutout to the helpful devs on the Selenium Slack/IRC channel (see (slack.com/selenium)[https://seleniumhq.slack.com/join/shared_invite/enQtODAwOTUzOTM5OTEwLTZjZjgzN2ExOTBmZGE0NjkwYzA2Nzc0MjczMGYwYjdiNGQ5YjI0ZjdjYjFhMjVlMjFkZWJmNDYyMmU1OTYyM2Y])
