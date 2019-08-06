from django.test import TestCase

# Create your tests here.
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from .models import Company

CHROME_DRIVER_PATH = f"driver/chromedriver"


class AccountTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        super(AccountTestCase, self).setUp()
        user1 = User.objects.create_user("testuser", "testuser@gmail.com", "testusersecret")
        user1.save()
        company1 = Company(name="company1", user=user1)
        company1.save()

    def tearDown(self):
        self.driver.quit()
        super(AccountTestCase, self).tearDown()
    
    def test_login(self):
        self.driver.get('%s%s' % (self.live_server_url, '/login'))
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys('testuser')
        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys('testusersecret')
        self.driver.find_element_by_name("_submit").click()
        
        self.assertIn("Home", self.driver.title)
    
    def test_signup(self):
        self.driver.get('%s%s' % (self.live_server_url, '/signup'))
        company_input = self.driver.find_element_by_name("company")
        company_input.send_keys('newcompany')
        
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys('newuser')
        
        email_input = self.driver.find_element_by_name("email")
        email_input.send_keys('newuser@yahoo.com')
        
        password1_input = self.driver.find_element_by_name("password1")
        password1_input.send_keys('secretuser&123')
        password2_input = self.driver.find_element_by_name("password2")
        password2_input.send_keys('secretuser&123')
        self.driver.find_element_by_name("_submit").click()
        
        new_user = User.objects.get(username='newuser')
        self.assertEquals(new_user.email, 'newuser@yahoo.com')
        self.assertIn("Home", self.driver.title)
