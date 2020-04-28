UNEDITED RAMBLINGS AS OF 2020-04-24
TODO- Clean this up and finish my incohorent, unfinished thoughts.

# STILL NEEDS TO BE EDITED/FINISHED
### DEVELOPMENT TIMELINE
MAJOR PHASES OF DEVELOPMENT:
- 1.) Prototyped homepage, genrepage, login, then videopage
- 2.) Converted everything to a POM design
- 3.) Optimized for speed by removing time.sleep()
- 4.) Converting 95% test accuracy to 99%+

### Locating Elements in Netflix's DOM
Less than 1 percent of Netflix's elements have "ID" attributes. This presents an interesting dilemma
for Selenium, since the number one recommended element locator is VIA ID. Netflix does, however,
provide a gorgeous alternative, namely a 'data-uia' attribute. 'data-uia' values range from 'my-list'
to 'upvote-button' to 'play-button'. Exactly the kind of thing we are looking for, unique identifiers 
THAT ARE HUMAN READABLE(and thus make test design drastically easier to read and debug)

### VIdeoPage state management- A surprisingly beautiful solution
At first, I was very afraid of the videopage and its associated tests. There are 5 basic 'states' of
the Netflix Akira player(idle, paused, credits-rolling, buffering), all of which can happen 
simultaneously. Managing each state with its own seperate function turned out to not to be as 
troublesome as first thought(e.g. if player is idle, wake up, else do nothing). These core 
'state-managing' functions found their way into almost every test (e.g. to pause the player, the
pause function first had to 1.) attempt to wake up the player if idle 2.) then find the pause 
button and click it). This "state management" solution turned out to work almost flawlessly and held
up after removing the training wheels(removing all of the time.sleep() commands and adding optimal
explicit waits)

### The nightmare of optimizing the HomePage-An unpleasant surprise
The Home page of netflix, (netflix.com/browse), was initially very pleasant to test. Sure, there
were some complications with the show-preview/bob-container(mousing over a show causes a small container
to open that flashes images of the show and displays a few buttons like play/upvote/addtomylist), but
they were quickly rectified by using ActionChains and mouse over tools. I had a rude awakening when
I went to optimize this page for speed. When I replaced all of the time.sleep() commands with more
natural waits(like wait for element to be present/visible), things quickly went down hill. The 
fundamental problem was that when oepning certain containers, 
certain elements(addtomylist button in particular) were fully visible, and causing the webDriverWaits
to finish, and were clickable, but 10% of the time the clicks were registering in the wrong
location. 

### Prototyped core tests in 6 days, 20 days to structure, beautify, and optimize
One of the nicer parts of this project was how fast I was able to prototype the tests. In 2 days I 
had tests for core features of the homepage up and running(play a show, upvote/downvote a show,
add a show to my list, scrape genre/tag/actor lists, etc.) and within 6 days I had tests for login,
homepage, and the videopage. The first results were littered with suboptimal waits, there wasnt a
single class anywhere, and the only way I could run a test was from the interactive prompt. Only 
after this point, when I knew it was possible to automate everything, was I comfortable rewritting
everything into a Page-Object-Model design.

### Funny Jenkins setup story- GCP blocking traffic by default
Spent hours debugging why Jenkins wasnt triggering new builds. The rabbit hole started:

THINGS I LEARNED:
- How to manually open ports
- How to set github webhooks for ci/cd 
- How to add ingress/egress rules for GCP
- The solution was to enable traffic through the specific port. GCP: "By default, incoming traffic
from outside your network is blocked"