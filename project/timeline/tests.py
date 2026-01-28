from django.test import TestCase
from .models import Year, Months
from django.core.exceptions import ValidationError

# Create your tests here.

class YearModelTest(TestCase):
    def test_fail_year_below_2025(self):
        year = Year(year=2024)
        with self.assertRaises(ValidationError):
            year.clean()

    def test_fail_year_above_2026(self):
        year = Year(year=2027)
        with self.assertRaises(ValidationError):
            year.clean()

    def test_accept_year_2025(self):
        year = Year(year=2025)
        try:
            year.clean()  # Should not raise ValidationError
        except ValidationError:
            self.fail("ValidationError raise because year should be 2025")
        

    def test_accept_year_2026(self):
        year =Year(year = 2026)
        try:
            year.clean()  # Should not raise ValidationError
        except ValidationError:
            self.fail("ValidationError raise because year should be 2026")


class MonthsModelTest(TestCase):
    def test_not_add_more_than_12_months(self):
        for i in range(12):
            month = Months.objects.create(name=f"Month {i+1}")
            month.clean()  # Should not raise ValidationError
            month.save()
            new_month = Months(name="Month 13")
            with self.assertRaises(ValidationError):
                new_month.clean()

