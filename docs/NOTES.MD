
https://github.com/aslushnikov/getting-started-with-cdp/blob/master/README.md

### TOPICS TO EXPLORE:
- chrome devtools PROTOCOL
- https://en.wikipedia.org/wiki/Microsoft_UI_Automation
- Netflix uses a cool UIA ID of the form `data-uia="myListButton"`


### PROBLEMS WITH CIRCLECI
- I'm not testing against a local version of Netflix's app (localhost:8000). This complicates 
pretty dramitically. TODO- NICE TO HAVE BUT A HUGE TIME SINK


https://gist.github.com/dariodiaz/3104601
<!-- # COOL HIGHLIST FUCNTION FOR DEBUGGING
# def highlight(element):
#     """Highlights (blinks) a Selenium Webdriver element"""
#     driver = element._parent
#     def apply_style(s):
#         driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
#                               element, s)
#     original_style = element.get_attribute('style')
#     apply_style("background: yellow; border: 2px solid red;")
#     time.sleep(.3)
#     apply_style(original_style) -->