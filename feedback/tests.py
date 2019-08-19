import unittest

from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from account.models import Company
from .models import Customer, Answer, Note

CHROME_DRIVER_PATH = f"driver/chromedriver"


class FeedbackTestCase(StaticLiveServerTestCase):
    def setUp(self):
        """Setup initial data"""
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        super(FeedbackTestCase, self).setUp()
        self.driver.implicitly_wait(50)

        user1 = User.objects.create_user("testuser", "testuser@gmail.com", "testusersecret")
        user1.save()
        company1 = Company(name="company1", user=user1)
        company1.save()
        customer1 = Customer(name="Ismahel", email="ismahel@gmail.com", cellphone="+237682363923",
                             company=company1)
        customer1.save()

        answer = Answer()
        answer.customer_answer = "I am very satisfied and will refer my friends and family to you"
        answer.comment = ""
        answer.customer = customer1
        answer.survey_id = 1
        answer.save()

    def tearDown(self):
        # self.driver.quit()
        # super(FeedbackTestCase, self).tearDown()
        pass

    def login(self):
        """Hanlde login"""
        self.driver.get('%s%s' % (self.live_server_url, '/login'))
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys('testuser')
        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys('testusersecret')
        self.driver.find_element_by_name("_submit").click()

    def test_view_home(self):
        self.driver.get('%s%s' % (self.live_server_url, ''))
        self.assertIn("Home", self.driver.title)

    def test_create_survey(self):
        self.login()
        self.driver.get('%s%s' % (self.live_server_url, '/create_survey'))
        name_input = self.driver.find_element_by_name("name")
        name_input.send_keys("Blandine")
        email_input = self.driver.find_element_by_name("email")
        email_input.send_keys("blandine@gmail.com")
        cellphone_input = self.driver.find_element_by_name("cellphone")
        cellphone_input.send_keys("+237679238472")
        self.driver.find_element_by_name("_submit").click()

        customer = Customer.objects.get(email="blandine@gmail.com")
        self.assertEqual(customer.name, "Blandine")

    def test_save_first_form(self):
        self.driver.get('%s%s' % (self.live_server_url, '/formA?email=ismahel@gmail.com'))
        # experience_choice = self.driver.find_element_by_name("experience")
        choice1 = self.driver.find_element_by_id("id_experience_0")
        choice1.click()

    def test_save_second_form(self):
        self.driver.get('%s%s' % (self.live_server_url, '/formB?email=ismahel@gmail.com'))


if __name__ == '__main__':
    unittest.main()
