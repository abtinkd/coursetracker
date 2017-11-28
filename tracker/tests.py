import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from django.test import LiveServerTestCase


class IntegrationTestCase(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

        # Mask long function names
        self.find_link, self.find_id, self.find_tag, = self.driver.find_element_by_link_text, \
                                                       self.driver.find_element_by_id, \
                                                       self.driver.find_elements_by_tag_name
        self.find_name, self.find_class_name = self.driver.find_element_by_name, self.driver.find_elements_by_class_name

        self.driver.get(self.live_server_url)
        for username, password in (('Marjan', 'CS541admin'), ('Abtin', 'CS541admin')):
            # Navigate to the signup page
            self.click('Sign Up')

            # Enter information
            self.find_id("id_username").send_keys(username)   # username
            self.find_id("id_password1").send_keys(password)  # password
            self.find_id("id_password2").send_keys(password)  # confirmation
            self.find_tag("button")[1].send_keys(Keys.RETURN)
            
            self.click('Log Out')

    def tearDown(self):
        self.driver.refresh()
        self.driver.close()

    def click(self, link_string):
        """Shortcut for clicking on navigation elements."""
        self.find_link(link_string).send_keys(Keys.RETURN)

    def log_in(self, username, password):
        """Go to the login page and log in as the given user."""
        self.click('Log In')
        self.find_id("id_username").send_keys(username)
        self.find_name("password").send_keys(password)
        self.find_name("Submit").send_keys(Keys.RETURN)

    def test_course_discretion(self):
        """Make sure that Users can only see their own Courses."""
        self.log_in(username='Abtin', password='CS541admin')
        self.click('Courses')  # Abtin goes to the Courses page

        # Now add the "Abtin" Course if it doesn't exist
        if not any([cell.text == "Abtin" for cell in self.find_class_name("name")]):
            self.find_id("id_name").send_keys("Abtin")
            self.find_id("id_hours").send_keys("10")
            self.find_name("create").send_keys(Keys.ENTER)
        self.click('Log Out')  # Abtin logs out

        self.log_in(username='Marjan', password='CS541admin')
        self.click('Courses')  # go to Courses

        # Search for a Course with name "Abtin"
        self.assertFalse(any([cell.text == "Abtin" for cell in self.find_class_name("name")]))

    def test_add_course_log_time(self):
        """Ensure the User can add a Course and log study time."""
        self.log_in(username='Marjan', password='CS541admin')
        self.click('Courses')  # go to the Courses page

        # Now add the "CS 1" Course if it doesn't exist
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

        # Check that History works
        for button_name in ('year', 'month', 'week', 'current'):  # check button presets
            self.click('History')
            self.find_name(button_name).send_keys(Keys.ENTER)

        # TODO test date entry?
