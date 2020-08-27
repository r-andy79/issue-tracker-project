from django.test import TestCase
from django.urls import reverse
from tickets.models import Ticket, Comment, Vote, Payment
# Create your tests here.

class IndexTest(TestCase):
    def test_status_200(self):
        url = reverse('tickets_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


def create_new_user_data(**kwargs):
    default_data = {
        'email': "joe@test.com",
        'email2': "joe@test.com",
        'username': "Joey",
        'password1': "Test456!",
        'password2': "Test456!"
    }
    # Data from kwargs overwrite specified keys in default data
    default_data.update(kwargs) 
    return default_data

class SignUpTest(TestCase):
    page_url = reverse('account_signup')
    success_url = reverse('account_email_verification_sent')
    
    def test_status_200(self):
        response = self.client.get(self.page_url)
        self.assertEqual(response.status_code, 200)

    
    def test_valid_data(self):
        data = create_new_user_data()
        response = self.client.post(self.page_url, data)
        self.assertRedirects(response, self.success_url)

    def test_invalid_passwords(self):
        data = create_new_user_data(
            password1='Test123!',
            password2='Test444!'
        )
        response = self.client.post(self.page_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You must type the same password each time.')

    def test_invalid_emails(self):
        data = create_new_user_data(
            email='joe@test.com',
            email2='joey@test.com'
        )
        response = self.client.post(self.page_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You must type the same email each time.')

    def test_not_unique_email(self):
        data = create_new_user_data(
            email='mike@test.com',
            email2='mike@test.com',
            username='Mike123'
        )
        response = self.client.post(self.page_url, data)
        self.assertEqual(response.status_code, 302)
        
        data = create_new_user_data(
            email='mike@test.com',
            email2='mike@test.com',
            username='Mike456'
        )
        response = self.client.post(self.page_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A user is already registered with this e-mail address.')

    def test_not_unique_username(self):
        data = create_new_user_data(
            email='jimmy@test.com',
            email2='jimmy@test.com',
            username='Mike123'
        )
        response = self.client.post(self.page_url, data)
        self.assertEqual(response.status_code, 302)
        
        data = create_new_user_data(
            email='mike@test.com',
            email2='mike@test.com',
            username='Mike123'
        )
        response = self.client.post(self.page_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A user with that username already exists.')

