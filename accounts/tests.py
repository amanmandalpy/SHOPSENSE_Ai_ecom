from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountsTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'StrongPassword123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_registration_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

        # Test duplicate email
        duplicate_data = self.user_data.copy()
        duplicate_data['username'] = 'testuser2'
        response = self.client.post(reverse('register'), duplicate_data)
        self.assertContains(response, 'A user with that email already exists.')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        
        login_success = self.client.login(username='testuser', password='StrongPassword123!')
        self.assertTrue(login_success)

    def test_profile_view_unauthenticated(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")

    def test_profile_update(self):
        self.client.login(username='testuser', password='StrongPassword123!')
        response = self.client.post(reverse('profile'), {
            'first_name': 'Updated',
            'last_name': 'Name',
            'phone': '1234567890',
            'preferred_currency': 'USD'
        })
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.preferred_currency, 'USD')
