from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import Transaction, CashTransaction, Profile, Instrument
from .forms import TransactionForm, CashTransactionForm
from django.conf import settings
from InvestAssistant.accounts.models import AppUser
import uuid


class TransactionModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a unique user (triggers Profile creation via signal)
        cls.user = AppUser.objects.create_user(
            email=f"testuser_{uuid.uuid4()}@example.com",
            password="testpass"
        )
        # Access the Profile created by the signal
        cls.profile = cls.user.profile
        cls.profile.balance = 10000 
        cls.profile.save()
        cls.instrument = Instrument.objects.create(name="Test Stock")

    def test_clean_quantity_zero_raises_error(self):
        transaction = Transaction(
            profile=self.profile,
            instrument=self.instrument,
            transaction_side="BUY",
            quantity=0,
            price_per_unit=Decimal("10.00")
        )
        with self.assertRaises(ValidationError):
            transaction.clean()

    def test_calculate_transaction_value(self):
        transaction = Transaction(
            profile=self.profile,
            instrument=self.instrument,
            transaction_side="BUY",
            quantity=Decimal("100.00"),
            price_per_unit=Decimal("15.00")
        )
        self.assertEqual(transaction.calculate_transaction_value(), Decimal("1500.00"))

    def test_str_representation(self):
        transaction = Transaction(
        profile=self.profile,
        instrument=self.instrument,
        transaction_side="BUY",
        quantity=Decimal("50.0000"),
        price_per_unit=Decimal("20.00")
        )
        transaction.save()  # Set timestamp
        expected = f"{transaction.transaction_side} {transaction.quantity:.4f} {transaction.instrument.name}"
        self.assertEqual(str(transaction), f"{transaction.timestamp}: {expected} by {self.profile.full_name or 'Anonymous'}")

    def test_invalid_transaction_side(self):
        transaction = Transaction(
            profile=self.profile,
            instrument=self.instrument,
            transaction_side="INVALID",
            quantity=Decimal("10.00"),
            price_per_unit=Decimal("10.00")
        )
        with self.assertRaises(ValidationError):
            transaction.full_clean()


class CashTransactionModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a unique user (triggers Profile creation via signal)
        cls.user = AppUser.objects.create_user(
            email=f"testuser_{uuid.uuid4()}@example.com",
            password="testpass"
        )
        # Access the Profile created by the signal
        cls.profile = cls.user.profile

    def test_str_representation(self):
        cash_transaction = CashTransaction(
            profile=self.profile,
            transaction_flow="DEPOSIT",
            amount=Decimal("1000.00")
        )
        self.assertIn(f"DEPOSIT {settings.DEFAULT_CURRENCY}1000.00", str(cash_transaction))

    def test_invalid_transaction_flow(self):
        cash_transaction = CashTransaction(
            profile=self.profile,
            transaction_flow="INVALID",
            amount=Decimal("500.00")
        )
        with self.assertRaises(ValidationError):
            cash_transaction.full_clean()

    def test_amount_negative_raises_error(self):
        cash_transaction = CashTransaction(
            profile=self.profile,
            transaction_flow="DEPOSIT",
            amount=Decimal("-100.00")
        )
        with self.assertRaises(ValidationError):
            cash_transaction.full_clean()


class TransactionFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a unique user (triggers Profile creation via signal)
        cls.user = AppUser.objects.create_user(
            email=f"testuser_{uuid.uuid4()}@example.com",
            password="testpass"
        )
        # Access the Profile created by the signal
        cls.profile = cls.user.profile
        cls.profile.balance = 1000
        cls.profile.save()
        cls.instrument = Instrument.objects.create(name="Test Stock")

    def test_valid_form(self):
        data = {
            "profile": self.profile.pk,
            "instrument": self.instrument,
            "transaction_side": "BUY",
            "quantity": "10.00",
            "price_per_unit": "15.00"
        }
        form = TransactionForm(data)
        self.assertTrue(form.is_valid())
        transaction = form.save()
        self.assertEqual(transaction.quantity, Decimal("10.00"))
        self.assertEqual(transaction.price_per_unit, Decimal("15.00"))

    def test_invalid_quantity_zero(self):
        data = {
            "profile": self.profile.pk,  
            "instrument": self.instrument.id,  
            "transaction_side": "BUY",
            "quantity": "0.00",
            "price_per_unit": "15.00"
        }
        form = TransactionForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("quantity", form.errors)

    def test_missing_required_field(self):
        data = {
            "profile": self.profile,
            "instrument": self.instrument,
            "transaction_side": "BUY",
            "price_per_unit": "15.00"
        }
        form = TransactionForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("quantity", form.errors)


class CashTransactionFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = AppUser.objects.create_user(
            email=f"testuser_{uuid.uuid4()}@example.com",
            password="testpass"
        )
        cls.profile = cls.user.profile
        cls.profile.balance = Decimal("10000.00")  # Use Decimal
        cls.profile.save()

    def test_valid_form(self):
        data = {
            "transaction_flow": "DEPOSIT",
            "amount": "500.00"
        }
        form = CashTransactionForm(data)
        self.assertTrue(form.is_valid())
        cash_transaction = form.save(commit=False)
        cash_transaction.profile = self.profile
        cash_transaction.save()
        self.assertEqual(cash_transaction.amount, Decimal("500.00"))
        self.assertEqual(cash_transaction.transaction_flow, "DEPOSIT")

    def test_invalid_amount_negative(self):
        data = {
            "transaction_flow": "DEPOSIT",
            "amount": "-100.00"
        }
        form = CashTransactionForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("amount", form.errors)

    def test_invalid_transaction_flow(self):
        data = {
            "transaction_flow": "INVALID",
            "amount": "500.00"
        }
        form = CashTransactionForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("transaction_flow", form.errors)


