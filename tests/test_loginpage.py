import unittest
import time

from selenium import webdriver

import secrets
import browserconfig
import pagemodels.loginpage


class LoginPageTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ launch the webdriver of choice with options/capabilties. (SEE browserconfig.py)"""
        if browserconfig.current_browser in ['chrome', 'firefox']:
            cls.driver = browserconfig.driver_runner(
                executable_path=browserconfig.driver_path,
                desired_capabilities=browserconfig.capabilities
            )
        elif browserconfig.current_browser == 'edge':
            cls.driver = browserconfig.driver_runner(
                executable_path=browserconfig.driver_path,
                desired_capabilities=browserconfig.capabilities  
            )

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        """navigate to the login page"""
        self.driver.get('https://www.netflix.com/login')

    def tearDown(self):
        """delete all cookies in case the login was successful"""
        self.driver.delete_all_cookies()

    # def test_correct_user_login(self):
    #     login_page = pagemodels.loginpage.LoginPage(self.driver)
    #     login_page.user_login(
    #         secrets.bradleys_email, secrets.bradleys_password
    #     )
    #     time.sleep(2)
    #     self.assertTrue(login_page.login_successful())

    def test_user_login_incorrect_password(self):
        """ correct email but incorrect password """
        login_page = pagemodels.loginpage.LoginPage(self.driver)
        login_page.fake_login(
            secrets.bradleys_email, "FAKEPASSWORD123"
        )
        time.sleep(2)
        self.assertFalse(login_page.login_successful())

    def test_user_login_incorrect_email(self):
        """ incorrect email but registered password """
        login_page = pagemodels.loginpage.LoginPage(self.driver)
        login_page.fake_login(
            "fakeemail@email.com", secrets.bradleys_password
        )
        time.sleep(2)
        self.assertFalse(login_page.login_successful())

    def test_no_credentials_submit(self):
        """ submit the completely blank email and password fields"""
        login_page = pagemodels.loginpage.LoginPage(self.driver)
        login_page.fake_login(
            "", ""
        )
        # Assert that the credentials are invalid (missing implies invalid)
        self.assertTrue(login_page.is_invalid_username)
        self.assertTrue(login_page.is_invalid_password)

# if __name__ == "__main__":
#     unittest.main()
