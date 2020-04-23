


### UI
Less than 1 percent of Netflix's elements have "ID" attributes. This presents an interesting dilemma
for Selenium, since the number one recommended element locator is VIA ID. Netflix does, however,
provide a gorgeous alternative, namely a 'data-uia' attribute. 'data-uia' values range from 'my-list'
to 'upvote-button' to 'play-button'. Exactly the kind of thing we are looking for, unique identifiers 
THAT ARE HUMAN READABLE(and thus make test design drastically easier to read and debug)
