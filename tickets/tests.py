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
        'username': "Joe",
        'password1': "Test456!",
        'password2': "Test456!"
    }
    # Dane z kwargs nadpisują wybrane klucze w default data
    default_data.update(kwargs) 
    return default_data

class SignUpTest(TestCase):
    def test_status_200(self):
        pass
    
    def test_valid_data(self):
        data = create_new_user_data()
        url = reverse('account_signup')
        response = self.client.post(url, data)
        print(response.content)
        print(response.status_code)
        self.assertEqual(0, 1)

    def test_invalid_passwords(self):
        pass

    def test_invalid_emails(self):
        pass

    def test_not_unique_email(self):
        pass

    def test_not_unique_username(self):
        pass

