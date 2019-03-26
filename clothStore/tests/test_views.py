from django.test import TestCase, Client, SimpleTestCase, LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import os
import random


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


class AccountTestCase(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(AccountTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(AccountTestCase, self).tearDown()

    def test_register_new_user(self):
        selenium = self.selenium;
        selenium.get('http://127.0.0.1:8000/register/')

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
        email.send_keys('joaogabriel.s.o@hotmail.com')
        password1.send_keys('P4$$W0RD69k')
        password2.send_keys('P4$$W0RD69k')

        #submitting the form
        submit.send_keys(Keys.RETURN)

        assert 'Check your email'
