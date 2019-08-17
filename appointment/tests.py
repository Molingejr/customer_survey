import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert

from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from .models import Company, Calendar, Appointment
from datetime import timedelta, datetime


CHROME_DRIVER_PATH = f"driver/chromedriver"
        
        
class CalendarTestCase(StaticLiveServerTestCase):
    def setUp(self):
        """Setup initial data"""
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        super(CalendarTestCase, self).setUp()
        self.driver.implicitly_wait(50)
        
        user1 = User.objects.create_user("testuser", "testuser@gmail.com", "testusersecret")
        user1.save()
        company1 = Company(name="company1", user=user1)
        company1.save()
        
        calendar = Calendar(provider_name="newuser", office_location="Mvog-mbi", slot_duration=timedelta(minutes=15),
                            working_days="2,3,4", start_time="08:00:00", end_time="18:00:00", company=company1)
        calendar.save()
        
        appointment = Appointment(mobilephone="+237674523054", email="user@gmail.com", first_name="Johnson",
                                  last_name="Micheal", notes="I need to discuss about my idea.",
                                  start_time="2019-08-15 09:00:00", end_time="2019-08-15 08:15:00", calendar=calendar)
        appointment.save()
        
    def tearDown(self):
        self.driver.quit()
        super(CalendarTestCase, self).tearDown()
        
    def login(self):
        """Hanlde login"""
        self.driver.get('%s%s' % (self.live_server_url, '/login'))
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys('testuser')
        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys('testusersecret')
        self.driver.find_element_by_name("_submit").click()
    
    def test_create_calendar(self):
        self.login()
        self.driver.get('%s%s' % (self.live_server_url, '/appointment/create_calendar'))
        provider_name_input = self.driver.find_element_by_name("provider_name")
        provider_name_input.send_keys('testuser1')
        office_location_input = self.driver.find_element_by_name("office_location")
        office_location_input.send_keys('molyko')
        slot_duration_input = self.driver.find_element_by_name("slot_duration")
        slot_duration_input.send_keys(Keys.BACKSPACE*8)
        slot_duration_input.send_keys('00:15:00')
        working_days_checkboxes = self.driver.find_element_by_name("working_days")
        all_options = self.driver.find_elements_by_class_name("form-check-input")
        
        for day in range(1, 7, 2):
            if not all_options[day].is_selected():
                all_options[day].click()
        
        start_time_input = self.driver.find_element_by_name("start_time")
        start_time_input.send_keys('8:00:00')
        end_time_input = self.driver.find_element_by_name("end_time")
        end_time_input.send_keys('18:00:00')
        
        self.driver.find_element_by_name("_submit").click()
        new_calendar = Calendar.objects.get(provider_name="testuser1")
        self.assertEquals(new_calendar.office_location, "molyko")
        
    def test_view_appointment_by_admin(self):
        self.login()
        self.driver.get('%s%s' % (self.live_server_url, '/appointment/calendar'))
        
        view_appointment_details_button = self.driver.find_element_by_link_text('View Details')
        view_appointment_details_button.click()
        self.assertIn("Appointments", self.driver.title)

    def test_view_appointment_by_anonymous(self):
        self.driver.get('%s%s' % (self.live_server_url, '/appointment/calendar/1'))
        self.assertIn("Appointments", self.driver.title)
    
    def test_schedule_appointment(self):
        self.driver.get('%s%s' % (self.live_server_url, '/appointment/calendar/1'))
        self.assertIn("ACME Company", self.driver.find_element_by_tag_name("h1").text)

        # Todo: Choose a slot and click accept on the pop-up box
        time_row = self.driver.find_element_by_css_selector('tr[data-time="11:00:00"]')
        action = ActionChains(self.driver)
        action.move_to_element_with_offset(time_row, time_row.rect['width']/2, time_row.rect['height']/2)
        action.click()
        action.perform()
     
        Alert(self.driver).accept()
        # WebDriverWait(self.driver, 5).until(EC.alert_is_present(),
        #                            'Timed out waiting for PA creation ' +
        #                            'confirmation popup to appear.')

        # alert = self.driver.switch_to.alert
        # alert.accept()
 
    def test_schedule(self):
        self.driver.get('%s%s' % (self.live_server_url, 
                                  '/appointment/calendar/1/details?start_time=2019-08-07T11:00:00Z&end_time=2019-08-07T11:15:00Z'))
        
        self.assertIn("Contact Form", self.driver.title) 
       
        mobilephone_input = self.driver.find_element_by_name("mobilephone")
        mobilephone_input.send_keys('+237677384133')
        email_input = self.driver.find_element_by_name("email")
        email_input.send_keys('jacob@gmail.com')
        first_name_input = self.driver.find_element_by_name("first_name")
        first_name_input.send_keys('Jacob')
        last_name_input = self.driver.find_element_by_name("last_name")
        last_name_input.send_keys('Ismahel')
        notes_input = self.driver.find_element_by_name("notes")
        notes_input.send_keys('I need a model of my business built')
        self.driver.find_element_by_name("_submit").click()
        
        new_appointment = Appointment.objects.get(mobilephone="+237677384133")
        self.assertEquals(new_appointment.first_name, "Jacob")


if __name__ == '__main__':
    unittest.main()
