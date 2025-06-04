from django.test import TestCase
from django.core.exceptions import ValidationError
from InvestAssistant.instruments.models import Instrument
from InvestAssistant.transactions.models import Transaction
from InvestAssistant.instruments.forms import CreateInstrumentForm, EditInstrumentForm, DeleteInstrumentForm


class InstrumentModelTests(TestCase):
    def test_name_max_length(self):
        instrument = Instrument(name="x" * 101, ticker="TEST", type="SECURITY", current_price=10.0)
        with self.assertRaises(ValidationError):
            instrument.full_clean()

    def test_ticker_uniqueness(self):
        Instrument.objects.create(name="Test1", ticker="TEST", type="SECURITY", current_price=10.0)
        instrument = Instrument(name="Test2", ticker="TEST", type="SECURITY", current_price=20.0)
        with self.assertRaises(ValidationError):
            instrument.full_clean()

    def test_ticker_max_length(self):
        instrument = Instrument(name="Test", ticker="TEST1234567", type="SECURITY", current_price=10.0)
        with self.assertRaises(ValidationError):
            instrument.full_clean()

    def test_current_price_max_digits(self):
        instrument = Instrument(name="Test", ticker="TEST", type="SECURITY", current_price=99999999999.9999)
        with self.assertRaises(ValidationError):
            instrument.full_clean()

    def test_type_choices(self):
        instrument = Instrument(name="Test", ticker="TEST", type="INVALID", current_price=10.0)
        with self.assertRaises(ValidationError):
            instrument.full_clean()

    def test_ticker_nullable(self):
        instrument = Instrument(name="Test", ticker=None, type="SECURITY", current_price=10.0)
        instrument.full_clean()
        self.assertIsNone(instrument.ticker)

    def test_ordering(self):
        Instrument.objects.create(name="Zebra", ticker="ZEB", type="SECURITY", current_price=10.0)
        Instrument.objects.create(name="Apple", ticker="AAPL", type="SECURITY", current_price=20.0)
        names = [instr.name for instr in Instrument.objects.all()]
        self.assertEqual(names, ["Apple", "Zebra"])

    def test_verbose_names(self):
        self.assertEqual(Instrument._meta.verbose_name, "Instrument")
        self.assertEqual(Instrument._meta.verbose_name_plural, "Instruments")

    def test_current_price_default(self):
        instrument = Instrument(name="Test", ticker="TEST", type="SECURITY")
        self.assertEqual(instrument.current_price, 0.0)


class CreateInstrumentFormTests(TestCase):
    def test_valid_form(self):
        data = {
            "name": "Apple",
            "ticker": "AAPL",
            "current_price": 150.50,
            "type": "SECURITY",
        }
        form = CreateInstrumentForm(data)
        self.assertTrue(form.is_valid())
        instrument = form.save()
        self.assertEqual(instrument.name, "Apple")
        self.assertEqual(instrument.ticker, "AAPL")

    def test_invalid_form(self):
        data = {
            "name": "x" * 101,
            "ticker": "TEST",
            "current_price": 150.50,
            "type": "INVALID",
        }
        form = CreateInstrumentForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("type", form.errors)


class EditInstrumentFormTests(TestCase):
    def setUp(self):
        self.instrument = Instrument.objects.create(
            name="Apple", ticker="AAPL", type="SECURITY", current_price=150.50
        )

    def test_edit_form(self):
        data = {
            "name": "Apple Inc",
            "ticker": "AAPL",
            "current_price": 160.00,
            "type": "SECURITY",
        }
        form = EditInstrumentForm(data, instance=self.instrument)
        self.assertTrue(form.is_valid())
        instrument = form.save()

        self.assertEqual(instrument.name, "Apple Inc")
        self.assertEqual(instrument.current_price, 160.00)


class DeleteInstrumentFormTests(TestCase):
    def setUp(self):
        self.instrument = Instrument.objects.create(
            name="Apple", ticker="AAPL", type="SECURITY", current_price=150.50
        )

    def test_read_only_fields(self):
        form = DeleteInstrumentForm(instance=self.instrument)
        for field in form.fields.values():
            self.assertTrue(field.widget.attrs.get('readonly', False))


class InstrumentQueryTests(TestCase):
    def setUp(self):
        Instrument.objects.create(name="Apple", ticker="AAPL", type="SECURITY", current_price=150.50)
        Instrument.objects.create(name="Bitcoin", ticker="BTC", type="CRYPTO", current_price=40000.00)

    def test_ticker_index(self):
        with self.assertNumQueries(1):
            Instrument.objects.filter(ticker="AAPL").exists()

    def test_type_index(self):
        with self.assertNumQueries(1):
            Instrument.objects.filter(type="SECURITY").exists()


class InstrumentEdgeCaseTests(TestCase):
    def test_negative_price(self):
        instrument = Instrument(name="Test", ticker="TEST", type="SECURITY", current_price=-10.0)
        with self.assertRaises(ValidationError):
            instrument.full_clean()

    def test_boundary_price(self):
        instrument = Instrument(name="Test", ticker="TEST", type="SECURITY", current_price=9999999999.9999)
        instrument.full_clean()
        self.assertEqual(float(instrument.current_price), 9999999999.9999)


    def test_empty_name(self):
        instrument = Instrument(name="", ticker="TEST", type="SECURITY", current_price=10.0)
        with self.assertRaises(ValidationError):
            instrument.full_clean()