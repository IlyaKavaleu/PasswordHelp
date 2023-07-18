from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, reverse_lazy


class TestPasswordTestCase(TestCase):
    """
    Test for check PASSWORD CONTROLLER,
    status code and template used
    """

    def test_view(self):
        path = reverse('password')
        response = self.client.get(path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'generator/password.html')


class TestHomeTestCase(TestCase):
    """
    Test for check HOME PAGE,
    status code and template used
    """

    def test_view(self):
        path = reverse('home')
        response = self.client.get(path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'generator/home.html')


class TestAboutTestCase(TestCase):
    """
    Test for check ABOUT PAGE,
    status code and template used
    """

    def test_view(self):
        path = reverse('about')
        response = self.client.get(path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'generator/about.html')


class TestRegisterTestCase(TestCase):
    """Tests for REGISTRATION"""

    def setUp(self):
        """general variables with help setUp"""
        self.path = reverse('register')
        self.data = {
            'username': 'username@123',
            'password1': '12345678@cat',
            'password2': '12345678@cat',
        }

    def test_user_register_succeess_get(self):
        """Check on status_code and used templates"""
        response = self.client.get(self.path)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_user_register_post_success(self):
        """
        Test for absence of a user, success register and if success, we redirects to
        home.html and check and the fact that he is present with success
        """
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())

        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(User.objects.filter(username=username).exists())


class TestContactTestCase(TestCase):
    """
    Test for check SEND EMAIL MESSAGE,
    status code and template used
    """

    def setUp(self):
        """general variables with help setUp"""
        self.path = reverse('password')
        self.response = self.client.get(self.path)
        self.data = {
            'name': 'username@123',
            'sername': 'jones',
            'email': 'GuidovanRossum@gmail.com',
        }

    def test_email_success_get(self):
        """Test to get the right code status and the right template"""
        self.assertEquals(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, 'generator/password.html')

    def test_email_success_post(self):
        """test to send a password to gmail, if successful, we get status code 200"""
        response = self.client.post(self.path, self.data)
        self.assertEquals(response.status_code, HTTPStatus.OK)

    def test_email_error_post(self):
        """Test for unsuccessful sending of the letter, in case of an error we remain on this page"""
        response = self.client.post(self.path, self.data)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, '', html=True)
