import unittest

import secrets
import browserconfig
import pagemodels.loginpage

# 2020-04-22 All tests passing
# Tests passed 5 executions in a row. v1 Ready to ship


class LoginPageTests(unittest.TestCase):
    """All of the test cases for successful and unsuccessful login attempts."""

    @classmethod
    def setUpClass(cls):
        """Launch the webdriver of choice with selected options(see browserconfig.py)."""
        if browserconfig.current_browser in ['chrome', 'firefox']:
            cls.driver = browserconfig.driver_runner(
                executable_path=browserconfig.driver_path,
                desired_capabilities=browserconfig.capabilities
            )
        elif browserconfig.current_browser == 'edge':
            cls.driver = browserconfig.driver_runner(
                executable_path=browserconfig.driver_path,
                capabilities=browserconfig.capabilities
            )

    @classmethod
    def tearDownClass(cls):
        """Closes the browser and shuts down the driver executable."""
        cls.driver.quit()

    def setUp(self):
        """Navigate to the login page."""
        self.driver.get('https://www.netflix.com/login')

    def tearDown(self):
        """Delete all cookies in case the login was successful."""
        self.driver.delete_all_cookies()

    def test_correct_user_login(self):
        """Attempt to login with valid credentials."""
        login_page = pagemodels.loginpage.LoginPage(self.driver)
        login_page.user_login(
            secrets.MY_EMAIL, secrets.MY_PASSWORD
        )

        self.assertTrue(login_page.login_successful())

    def test_user_login_incorrect_password(self):
        """Attempt to login with a correct email but incorrect password."""
        login_page = pagemodels.loginpage.LoginPage(self.driver)
        login_page.fake_login(
            secrets.MY_EMAIL, "FAKEPASSWORD123"
        )

        self.assertFalse(login_page.login_successful())

    def test_user_login_incorrect_email(self):
        """Attempty to login with an incorrect email but a correct password."""
        login_page = pagemodels.loginpage.LoginPage(self.driver)
        login_page.fake_login(
            "fakeemail@email.com", secrets.MY_PASSWORD
        )

        self.assertFalse(login_page.login_successful())

    def test_no_credentials_submit(self):
        """Submit blank email and password fields."""
        login_page = pagemodels.loginpage.LoginPage(self.driver)
        login_page.submit_empty_fields()

        # Assert that the credentials are invalid (missing also implies invalid)
        self.assertTrue(login_page.is_invalid_username)
        self.assertTrue(login_page.is_invalid_password)

# if __name__ == "__main__":
#     unittest.main()
