from django.test import TestCase, Client, SimpleTestCase, LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
import unittest
import os
import random
from django.contrib.auth.models import User

# Create your tests here.

class PagesUpTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_is_up(self):
        """Tests if the index page is up"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register_is_up(self):
        """Tests if the registration page is up"""
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_login_is_up(self):
        """Tests if login page is up"""
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)


class AccountTestCase(StaticLiveServerTestCase):
    def setUp(self):
        super(AccountTestCase, self).setUp()
        # self.selenium = webdriver.Firefox()
        self.selenium = WebDriver()

    def tearDown(self):
        self.selenium.quit()
        super(AccountTestCase, self).tearDown()

    def test_register_new_user(self):
        selenium = self.selenium;
        selenium.get('%s%s' % (self.live_server_url, '/register/'))

        # first_name = selenium.find_element_by_id('id_first_name')
        # last_name = selenium.find_element_by_id('id_last_name')

        user = 'user' + str(random.randint(1,10000))

        username = selenium.find_element_by_id('id_username')
        email = selenium.find_element_by_id('id_email')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')

        submit = selenium.find_element_by_id('register-button')

        #Fill the form with data
        # first_name.send_keys('Jobalda')
        # last_name.send_keys('Unary')
        username.send_keys(user)
        email.send_keys(os.getenv('TESTING_EMAIL'))
        password1.send_keys('P4$$W0RD6k')
        password2.send_keys('P4$$W0RD6k')

        #submitting the form
        submit.click()
        self.assertEqual(selenium.current_url, '%s%s' % (self.live_server_url, '/register/complete/'))

    def test_login_user(self):
        username = 'usernamexTest'
        password= 'P4ssW0rdk0l'

        user = User.objects.create_user(username, 'test@mail.com', password)
        selenium = self.selenium;
        selenium.get('%s%s' % (self.live_server_url, '/login/'))

        usernameField= selenium.find_element_by_id('id_username')
        passwordField = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('submit')

        usernameField.send_keys(username)
        passwordField.send_keys(password)

        submit.click()
        self.assertEqual(selenium.current_url, '%s%s' % (self.live_server_url, '/'))
