from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Months(models.Model):
    name = models.CharField(max_length=20)

    def clean(self):
        if Months.objects.count() >=12:
            raise ValidationError("Cannot add Month More Than 12 months.")

    def __str__(self):
        return self.name  


class Year(models.Model):
    year = models.IntegerField()

    def clean(self):
        if self.year <2025 or self.year >2026:
            raise ValidationError("Year must be between 2025 and 2026.")

    def __str__(self):
        return str(self.year)         
