# GUIDE
- "I HAVE NO IDEA WHAT IM LOOKING AT." Watch https://gyazo.com/37be44a9993676c4161adff157960e45 then
checkout ./tests/test_videopage.py , it contains straightforward tests(mute, pause, add subtitles, etc.)
- This test suite is organized in a Page-Object-Model(POM) design pattern. TLDR: tests contain the 
test logic (asserts, etc.), Page objects (in /pagemodels/) hold the logic for interacting with the page.
- This design pattern(POM) is most the verbose(and the most complex) to write, but is the easiest to 
maintain in both speed and complexity. See https://www.selenium.dev/documentation/en/guidelines_and_recommendations/page_object_models/ 

# EXAMPLE
- Watch VIDEO TESTS https://gyazo.com/37be44a9993676c4161adff157960e45
- WATCH HOME PAGE TESTS https://gyazo.com/6821682827f79a47ce16e66c34ce2fbb
- HEADER TOOLS TESTS https://gyazo.com/b20fd223076bf34c1f2c9b94a4f1fe0a





# SETUP
I like to keep chrome and ChromeDriver as up to date as possible.
- Current google chrome version: "Version 81.0.4044.92 (Official Build) (64-bit)"
- Current ChromeDriver version: "81.0.4044.69"
https://chromedriver.storage.googleapis.com/index.html?path=81.0.4044.69/
- Execute tests exactly the same way normal unittest are executed 
`python -m unittest -v tests/test_videopage.py`
- geckodriver-v0.26.0-win64 , Firefox V 75.0 (64-bit)
## DEAR NETFLIX DEVS:
The purpose of this repo is to provide advance searching to users, an area in which your current
app falls short unfortunately. A perfect example is sorting a category by additional characteristics
(e.g. sorting Action movies by tag='Exciting'). In your current app, a user can sort movies by tag or sort by
genre, but not sort genre by tag.

Or you could always reopen the public API! 

Please kindly email me if you have any questions or concerns bradleypelton@gmail.com

