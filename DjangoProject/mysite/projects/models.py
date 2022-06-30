from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Employee(models.Model):
    SEX_CHOICES = (
        ('F', 'Female',),
        ('M', 'Male',),
        ('U', 'Unsure',),
    )

    first_name = models.CharField(max_length=200, null=False, blank=False)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, null=False, blank=False)
    phone = PhoneNumberField(null=False, blank=False, unique=True)

    def __str__(self):
        return self.first_name + " " + self.last_name