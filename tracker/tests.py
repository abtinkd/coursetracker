from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class IntegrationTestCase(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

        # Mask long function names
        self.find_link, self.find_id, self.find_tag, = self.driver.find_element_by_link_text, \
                                                       self.driver.find_element_by_id, \
                                                       self.driver.find_elements_by_tag_name
        self.find_name, self.find_class_name = self.driver.find_element_by_name, self.driver.find_elements_by_class_name

        self.driver.get(self.live_server_url)
        self.sign_up('Marjan', 'CS541admin')

    def tearDown(self):
        try:
            self.driver.close()
        except (TypeError, ConnectionAbortedError, ConnectionResetError):
            pass

    def click(self, link_string):
        """Shortcut for clicking on navigation elements."""
        self.find_link(link_string).send_keys(Keys.RETURN)

    def log_in(self, username, password):
        """Go to the login page and log in as the given user."""
        self.click('Log In')
        self.find_id("id_username").send_keys(username)
        self.find_name("password").send_keys(password)
        self.find_name("Submit").send_keys(Keys.RETURN)

    def sign_up(self, username, password):
        """Signs the user up and stays logged in."""
        self.click('Sign Up')

        # Enter information
        self.find_id("id_username").send_keys(username)  # username
        self.find_id("id_password1").send_keys(password)  # password
        self.find_id("id_password2").send_keys(password)  # confirmation
        self.find_tag("button")[1].send_keys(Keys.RETURN)

    def test_course_discretion(self):
        """Make sure that Users can only see their own Courses."""
        self.click('Log Out')
        self.sign_up(username='Abtin', password='CS541admin')
        self.log_in(username='Abtin', password='CS541admin')

        # Go to the Courses page and add the "Abtin" Course if it doesn't exist
        self.click('Courses')
        if not any([cell.text == "Abtin" for cell in self.find_class_name("name")]):
            self.find_id("id_name").send_keys("Abtin")
            self.find_id("id_hours").send_keys("10")
            self.find_name("create").send_keys(Keys.ENTER)
        self.click('Log Out')  # Abtin logs out

        self.log_in(username='Marjan', password='CS541admin')
        self.click('Courses')  # go to Courses

        # Search for a Course with name "Abtin"
        self.assertFalse(any([cell.text == "Abtin" for cell in self.find_class_name("name")]))

    def test_course_timer_history(self):
        """Ensure the User can add a Course, log study time, and view  History."""
        self.log_in(username='Marjan', password='CS541admin')

        # Go to the Courses page and add the "CS 1" Course if it doesn't exist
        self.click('Courses')
        if not any([cell.text == "CS 1" for cell in self.find_class_name("name")]):
            self.find_id("id_name").send_keys("CS 1")
            self.find_id("id_hours").send_keys("18")
            self.find_name("create").send_keys(Keys.ENTER)

        # Go to the Timer page, select the "CS 1" Course, and start the Timer
        self.click('Timer')
        Select(self.find_id("id_course")).select_by_visible_text("CS 1")
        self.find_id("playpause").send_keys(Keys.ENTER)

        # Stop the Timer
        self.find_id("stopbutton").send_keys(Keys.ENTER)

        # Check that History presets work
        for button_name in ('year', 'month', 'week', 'current'):  # check button presets
            self.click('History')
            self.find_name(button_name).send_keys(Keys.ENTER)

        # Check that custom History date ranges work - just make sure both calendars pop up
        self.click('History')
        self.assertEqual(len(self.driver.find_elements_by_xpath("//div[@class='datetimepicker-days']")), 2)
