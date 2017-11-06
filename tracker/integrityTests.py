import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

class Login_AddCourse_Timer(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()



    def test_Login_AddCourse_Timer(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        #should navigate to the login page
        self.assertIn("Please Sign In", driver.page_source)



        user_name = driver.find_element_by_id("id_username")
        password = driver.find_element_by_name("password")
        submit_login = driver.find_element_by_name("Submit")

        user_name.clear()
        password.clear()
        user_name.send_keys("Marjan")
        password.send_keys("CS541admin")
        submit_login.send_keys(Keys.RETURN)
        #check user could login successfully
        self.assertNotIn("Please enter a correct username and password", driver.page_source)

        #Go to the courses Page
        courses_link = driver.find_element_by_link_text('Courses')
        courses_link.send_keys(Keys.RETURN)

        # Now add the course with name "Course Marjan" if it does not exist
        find = False
        for cell in driver.find_elements_by_class_name("name"):
            if cell.text == "Course Marjan":
                find = True
                break
        if find == False:
            course_name = driver.find_element_by_id("id_name")
            course_hours = driver.find_element_by_id("id_hours")
            submit_course = driver.find_element_by_name("create")

            course_name.clear()
            course_hours.clear()

            course_name.send_keys("Course Marjan")
            course_hours.send_keys("18")
            submit_course.send_keys(Keys.ENTER)

        # Go to the Timer Page
        timer_link = driver.find_element_by_link_text('Timer')
        timer_link.send_keys(Keys.RETURN)

        #select the course "Course Marjan"
        select = Select(driver.find_element_by_id("id_course"))
        select.select_by_visible_text("Course Marjan")

        # Press start timer
        start_button = driver.find_element_by_id("playpause")
        start_button.send_keys(Keys.ENTER)

        time.sleep(40)

        # Press stop timer
        stop_button = driver.find_element_by_id("stopbutton")
        stop_button.send_keys(Keys.ENTER)

        #Log out
        logout_link = driver.find_element_by_link_text('Log out')
        logout_link.send_keys(Keys.RETURN)

        #You have logged out
        self.assertIn("You have logged out", driver.page_source)


    def tearDown(self):
       self.driver.close()

if __name__ == "__main__":
    unittest.main()


