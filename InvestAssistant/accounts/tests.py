from django.test import TestCase
from django import forms
from InvestAssistant.accounts.forms import CustomAuthenticationForm, AppUserRegistrationForm, ProfileEditForm
from InvestAssistant.accounts.models import AppUser, Profile    
from django.contrib.auth import get_user_model
import uuid


class TestCustomAuthenticationForm(TestCase):
    def setUp(self):
        self.user = AppUser.objects.create_user(email='test@example.com', password='testpassword123')
        self.form_data = {'username': 'test@example.com', 'password': 'testpassword123'}

    def test_form_fields_existence(self):
        form = CustomAuthenticationForm()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)

    def test_form_fields_attributes(self):
        form = CustomAuthenticationForm()
        self.assertEqual(form.fields['username'].widget.attrs['placeholder'], 'Email Address')
        self.assertEqual(form.fields['password'].widget.attrs['placeholder'], 'Password')

    def test_valid_form(self):
        form = CustomAuthenticationForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_credentials(self):
        data = {'username': 'test@example.com', 'password': 'wrongpassword'}
        form = CustomAuthenticationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)  # Check for authentication error


class TestAppUserRegistrationForm(TestCase):
    def setUp(self):
        self.valid_data = {
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

    def test_form_fields_existence(self):
        form = AppUserRegistrationForm()
        self.assertEqual(set(form.fields.keys()), {'email', 'password1', 'password2'})

    def test_form_fields_attributes(self):
        form = AppUserRegistrationForm()
        self.assertEqual(form.fields['email'].widget.attrs['placeholder'], 'Enter your email address')
        self.assertEqual(form.fields['password1'].widget.attrs['placeholder'], 'Create a password')

    def test_valid_form_saves_user(self):
        form = AppUserRegistrationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.email, 'newuser@example.com')

    def test_invalid_email(self):
        data = self.valid_data.copy()
        data['email'] = 'invalid-email'
        form = AppUserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_password_mismatch(self):
        data = self.valid_data.copy()
        data['password2'] = 'differentpassword'
        form = AppUserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)


class TestProfileEditForm(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email=f"testuser_{uuid.uuid4()}@example.com",
            password="testpass"
        )
        self.profile = self.user.profile
        self.profile.first_name = "John"
        self.profile.last_name = "Doe"
        self.profile.phone_number = "1234567890"
        self.profile.save()
        self.valid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '1234567890'
        }

    def test_form_fields_existence(self):
        form = ProfileEditForm()
        self.assertEqual(set(form.fields.keys()), {'first_name', 'last_name', 'phone_number'})

    def test_form_fields_attributes(self):
        form = ProfileEditForm()
        self.assertEqual(form.fields['first_name'].widget.attrs['placeholder'], 'First Name')

    def test_phone_number_validation(self):
        data = self.valid_data.copy()
        data['phone_number'] = 'invalid-phone'
        form = ProfileEditForm(data=data, instance=self.profile)
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)

    def test_valid_form_saves_profile(self):
        form = ProfileEditForm(data=self.valid_data, instance=self.profile)
        self.assertTrue(form.is_valid())
        profile = form.save()
        self.assertEqual(profile.first_name, 'John')
        self.assertEqual(profile.phone_number, '1234567890')

        