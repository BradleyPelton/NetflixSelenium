# EVERY PAGE IS SUPPOSED TO INHERIT FROM THIS basepage


class BasePage(object):
    """Base class to store default page settings."""

    def __init__(self, driver):
        self.driver = driver
