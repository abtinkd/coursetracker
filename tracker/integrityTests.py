import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

class Login_AddCourse_Timer(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    # Sign up for user one
    def test_SingUp_LOGIN_User1(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")

        # should navigate to the Sign up  page
        signup_link = driver.find_element_by_link_text('Sign Up')
        signup_link.send_keys(Keys.RETURN)

        user_name = driver.find_element_by_id("id_username")
        password = driver.find_element_by_id("id_password1")
        confirm_password = driver.find_element_by_id("id_password2")
        submit = driver.find_elements_by_tag_name("button")[1]
        user_name.clear()
        password.clear()
        confirm_password.clear()

        user_name.send_keys("Marjan")
        password.send_keys("CS541admin")
        confirm_password.send_keys("CS541admin")

        submit.send_keys(Keys.RETURN)


    def test_SingUp_LOGIN_User2(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")

        # should navigate to the Sign up  page
        signup_link = driver.find_element_by_link_text('Sign Up')
        signup_link.send_keys(Keys.RETURN)

        user_name = driver.find_element_by_id("id_username")
        password = driver.find_element_by_id("id_password1")
        confirm_password = driver.find_element_by_id("id_password2")
        submit = driver.find_elements_by_tag_name("button")[1]
        user_name.clear()
        password.clear()
        confirm_password.clear()

        user_name.send_keys("Abtin")
        password.send_keys("CS541admin")
        confirm_password.send_keys("CS541admin")

        submit.send_keys(Keys.RETURN)




    #user can see their own courses
    def test_User_Cannot_See_Others_Course(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        #should navigate to the login page
        self.assertIn("Please Sign In", driver.page_source)

        #Abtin logs in
        user_name = driver.find_element_by_id("id_username")
        password = driver.find_element_by_name("password")
        submit_login = driver.find_element_by_name("Submit")

        user_name.clear()
        password.clear()
        user_name.send_keys("Abtin")
        password.send_keys("CS541admin")
        submit_login.send_keys(Keys.RETURN)
        #check user could login successfully
        self.assertNotIn("Please enter a correct username and password", driver.page_source)

        #Abtin goes to the courses Page
        courses_link = driver.find_element_by_link_text('Courses')
        courses_link.send_keys(Keys.RETURN)

        # Now adds the course with name "Course Abtin" if it does not exist
        find = False
        for cell in driver.find_elements_by_class_name("name"):
            if cell.text == "Course Abtin":
                find = True
                break
        if find == False:
            course_name = driver.find_element_by_id("id_name")
            course_hours = driver.find_element_by_id("id_hours")
            submit_course = driver.find_element_by_name("create")

            course_name.clear()
            course_hours.clear()

            course_name.send_keys("Course Abtin")
            course_hours.send_keys("10")
            submit_course.send_keys(Keys.ENTER)

        #Abtin Loqs out
        logout_link = driver.find_element_by_link_text('Log out')
        logout_link.send_keys(Keys.RETURN)

        #Marjan Logs in
        login_link = driver.find_element_by_link_text('Log in')
        login_link.send_keys(Keys.RETURN)

        user_name = driver.find_element_by_id("id_username")
        password = driver.find_element_by_name("password")
        submit_login = driver.find_element_by_name("Submit")

        user_name.clear()
        password.clear()
        user_name.send_keys("Marjan")
        password.send_keys("CS541admin")
        submit_login.send_keys(Keys.RETURN)

        # Marjan goes to the courses Page
        courses_link = driver.find_element_by_link_text('Courses')
        courses_link.send_keys(Keys.RETURN)

        # Marjan searches for a course with name "Course Abtin"
        for cell in driver.find_elements_by_class_name("name"):
            if cell.text == "Course Abtin":
                return False;


        return  True

    #user can login in to te system, add a course and log a study time for that course
    def test_Login_AddCourse_Timer(self):

        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        # should navigate to the login page
        self.assertIn("Please Sign In", driver.page_source)

        user_name = driver.find_element_by_id("id_username")
        password = driver.find_element_by_name("password")
        submit_login = driver.find_element_by_name("Submit")

        user_name.clear()
        password.clear()
        user_name.send_keys("Marjan")
        password.send_keys("CS541admin")
        submit_login.send_keys(Keys.RETURN)
        # check user could login successfully
        self.assertNotIn("Please enter a correct username and password", driver.page_source)

        # Go to the courses Page
        courses_link = driver.find_element_by_link_text('Courses')
        courses_link.send_keys(Keys.RETURN)

        # Now add the course with name "Course Marjan" if it does not exist
        find = False
        for cell in driver.find_elements_by_class_name("name"):
            if cell.text == "CS 1":
                find = True
                break
        if find == False:
            course_name = driver.find_element_by_id("id_name")
            course_hours = driver.find_element_by_id("id_hours")
            submit_course = driver.find_element_by_name("create")

            course_name.clear()
            course_hours.clear()

            course_name.send_keys("CS 1")
            course_hours.send_keys("18")
            submit_course.send_keys(Keys.ENTER)

        # Go to the Timer Page
        timer_link = driver.find_element_by_link_text('Timer')
        timer_link.send_keys(Keys.RETURN)

        # select the course "CS 1"
        select = Select(driver.find_element_by_id("id_course"))
        select.select_by_visible_text("CS 1")

        # Press start timer
        start_button = driver.find_element_by_id("playpause")
        start_button.send_keys(Keys.ENTER)

        time.sleep(40)

        # Press stop timer
        stop_button = driver.find_element_by_id("stopbutton")
        stop_button.send_keys(Keys.ENTER)

        # Log out
        logout_link = driver.find_element_by_link_text('Log out')
        logout_link.send_keys(Keys.RETURN)

        # You have logged out
        self.assertIn("You have logged out", driver.page_source)


    def tearDown(self):
       self.driver.close()

if __name__ == "__main__":
    unittest.main()


