from __future__ import unicode_literals
from django.db import models
from localflavor.us.models import USStateField, PhoneNumberField, USZipCodeField, USSocialSecurityNumberField

GENDER_CHOICES = (
    ('MALE', 'Male'),
    ('FEMALE', 'Female'),
)

class UserSignupPlus(models.Model):
	email_address = models.EmailField(verbose_name=('Email address'), max_length=254, unique=True, null=False)
	city = models.CharField(verbose_name=('City'), max_length=64, blank=False, null=False)
	country = models.CharField(verbose_name=('Country'), max_length=100, blank=False, null=False)
	state = USStateField(verbose_name=('State'), max_length=100, blank=False, null=False)
	zip_code = USZipCodeField(verbose_name=('Zip code'), max_length=5, blank=False, null=False)
	home_phone = PhoneNumberField(verbose_name=('Phone number'), max_length=100, blank=False, null=False)
	birth_date = models.DateField(verbose_name=('BirthDate')) #no later than 100 years ago
	gender = models.CharField(verbose_name=('Gender'), max_length=20, choices=GENDER_CHOICES, blank=False, null=False)

