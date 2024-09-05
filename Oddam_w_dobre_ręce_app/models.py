from django.db import models
from django.contrib.auth.models import User

from phone_field import PhoneField


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Type(models.TextChoices):
        FUNDACJA = "FF",
        ORGANIZACJA_POZARZĄDOWA = "OP",
        ZBIÓRKA_LOKALNA = "ZL",

    type = models.CharField(choices=Type.choices, default=Type.FUNDACJA, max_length=2)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.PositiveSmallIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField()
    phone_number = PhoneField(blank=True)
    city = models.CharField(max_length=32)
    zip_code = models.CharField(max_length=5)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.address
