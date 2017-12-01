from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class IntegrationTestCase(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.live_server_url)

        # Mask long function names
        self.find_id, self.find_name = self.driver.find_element_by_id, self.driver.find_element_by_name

        # Sign up test user
        self.click('Sign Up')
        self.find_id("id_username").send_keys('admin')  # username
        self.find_id("id_password1").send_keys('CS561Admin')  # password
        self.find_id("id_password2").send_keys('CS561Admin')  # confirmation
        self.driver.find_elements_by_tag_name("button")[1].send_keys(Keys.RETURN)

    def tearDown(self):
        self.driver.refresh()
        try:
            self.driver.close()
        except (TypeError, ConnectionAbortedError, ConnectionResetError):
            pass

    def click(self, link_string):
        """Shortcut for clicking on navigation elements."""
        self.driver.find_element_by_link_text(link_string).send_keys(Keys.RETURN)

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
        def select_dates():
            for datepicker, date_id in zip(self.driver.find_elements_by_xpath("//div[@class='datetimepicker-days']"),
                                           ('id_start_date', 'id_end_date')):
                self.find_id(date_id).click()
                datepicker.find_elements_by_tag_name('td')[10].click()
        self.click('History')
        select_dates()
        self.find_name('custom').click()

        # Check CoursePerformance
        self.click('Course Performance')
        select_dates()
        Select(self.find_id("id_course")).select_by_visible_text("Test")
        self.find_name('custom').click()
