from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser


class Country(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    dial_code = models.CharField(max_length=250, null=True, blank=True)
    code = models.CharField(max_length=250, null=True, blank=True)
    img = models.ImageField(upload_to='country', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "country_table"


class Gender(models.Model):
    name= models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "gender_table"


class CustomUser(AbstractUser):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=250, null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "user_table"