from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class IntegrationTestCase(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.live_server_url)

        # Mask long function names
        self.find_link, self.find_id, self.find_tag, = self.driver.find_element_by_link_text, \
                                                       self.driver.find_element_by_id, \
                                                       self.driver.find_elements_by_tag_name
        self.find_name, self.find_class_name = self.driver.find_element_by_name, self.driver.find_elements_by_class_name

        self.sign_up('Marjan', 'CS541admin')

    def tearDown(self):
        self.driver.refresh()
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
        # Go to the Courses page and add the "Marjan" Course
        self.find_id("id_name").send_keys("Marjan")
        self.find_id("id_hours").send_keys("10")
        self.find_name("create").send_keys(Keys.ENTER)

        # Switch to Abtin
        self.click('Log Out')
        self.sign_up(username='Abtin', password='CS541admin')

        # Search for a Course with the name "Marjan"
        self.assertFalse(any([cell.text == "Marjan" for cell in self.find_class_name("name")]))

    def test_navigation(self):
        """Ensure the User can navigate between all the major parts of the website."""
        # Go to the Courses page and add a Course
        self.find_id("id_name").send_keys("Test")
        self.find_id("id_hours").send_keys("18")
        self.find_name("create").send_keys(Keys.ENTER)

        # Go to the Timer page, select the Course, and toggle the Timer
        self.click('Timer')
        Select(self.find_id("id_course")).select_by_visible_text("Test")
        self.find_id("playpause").send_keys(Keys.ENTER)
        self.find_id("stopbutton").send_keys(Keys.ENTER)

        # Check that History presets work
        for button_name in ('year', 'month', 'week', 'current'):
            self.click('History')
            self.find_name(button_name).send_keys(Keys.ENTER)

        # Check that custom History date ranges work
        self.click('History')
        for datepicker, date_id in zip(self.driver.find_elements_by_xpath("//div[@class='datetimepicker-days']"),
                                       ('id_start_date', 'id_end_date')):
            self.find_id(date_id).click()
            datepicker.find_elements_by_tag_name('td')[10].click()
        self.find_name('custom').click()
