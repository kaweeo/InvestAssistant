from django.test import TestCase
from django import forms
from InvestAssistant.accounts.forms import CustomAuthenticationForm, AppUserRegistrationForm, ProfileEditForm
from InvestAssistant.accounts.models import AppUser, Profile


class TestCustomAuthenticationForm(TestCase):
    def setUp(self):
        self.form = CustomAuthenticationForm()
        self.valid_data = {
            'username': 'test@example.com',
            'password': 'testpassword123'
        }

    def test_form_fields_existence(self):
        """Test that form has the expected fields"""
        self.assertIn('username', self.form.fields)
        self.assertIn('password', self.form.fields)

    def test_form_fields_attributes(self):
        """Test fields have correct attributes"""
        # Test username field
        username_field = self.form.fields['username']
        self.assertEqual(
            username_field.widget.attrs['placeholder'],
            'Email Address'
        )
        self.assertEqual(
            username_field.help_text,
            'Enter your email address to log in.'
        )

        # Test password field
        password_field = self.form.fields['password']
        self.assertEqual(
            password_field.widget.attrs['placeholder'],
            'Password'
        )
        self.assertEqual(
            password_field.help_text,
            'Enter your password to access your account.'
        )

    def test_form_field_types(self):
        """Test that fields use correct widget types"""
        self.assertIsInstance(
            self.form.fields['username'].widget,
            forms.TextInput
        )
        self.assertIsInstance(
            self.form.fields['password'].widget,
            forms.PasswordInput
        )


class TestAppUserRegistrationForm(TestCase):
    def setUp(self):
        self.form = AppUserRegistrationForm()

    def test_form_fields_existence(self):
        """Test that form has the expected fields"""
        expected_fields = {'email', 'password1', 'password2'}
        self.assertEqual(set(self.form.fields.keys()), expected_fields)

    def test_form_fields_attributes(self):
        """Test fields have correct attributes"""
        # Test email field
        email_field = self.form.fields['email']
        self.assertEqual(
            email_field.widget.attrs['placeholder'],
            'Enter your email address'
        )
        self.assertEqual(
            email_field.widget.attrs['class'],
            'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent'
        )

        # Test password1 field
        password1_field = self.form.fields['password1']
        self.assertEqual(
            password1_field.widget.attrs['placeholder'],
            'Create a password'
        )

        # Test password2 field
        password2_field = self.form.fields['password2']
        self.assertEqual(
            password2_field.widget.attrs['placeholder'],
            'Confirm your password'
        )

    def test_form_meta_attributes(self):
        """Test Meta class attributes"""
        self.assertEqual(self.form._meta.model, AppUser)
        self.assertEqual(
            self.form._meta.fields,
            ('email', 'password1', 'password2')
        )


class TestProfileEditForm(TestCase):
    def setUp(self):
        self.form = ProfileEditForm()

    def test_form_fields_existence(self):
        """Test that form has the expected fields"""
        expected_fields = {'first_name', 'last_name', 'phone_number'}
        self.assertEqual(set(self.form.fields.keys()), expected_fields)

    def test_form_fields_attributes(self):
        """Test fields have correct placeholders"""
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone_number': 'Phone Number'
        }

        for field_name, expected_placeholder in placeholders.items():
            self.assertEqual(
                self.form.fields[field_name].widget.attrs['placeholder'],
                expected_placeholder
            )

    def test_form_meta_attributes(self):
        """Test Meta class attributes"""
        self.assertEqual(self.form._meta.model, Profile)
        self.assertEqual(
            set(self.form._meta.fields),
            {'first_name', 'last_name', 'phone_number'}
        )