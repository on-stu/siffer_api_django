
from re import T
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import BooleanField, CharField, IntegerField, TextField
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(blank=True, null=True, max_length=150)
    userSize = models.TextField(blank=True, default="")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Site(models.Model):
    sitename = CharField(max_length=100, default="", blank=True)
    classname = CharField(max_length=100, default="", blank=True)
    match = CharField(max_length=100, default="", blank=True)
    encoding = CharField(max_length=100, default="", blank=True)
    iframe = BooleanField(default=False)
    standard = CharField(max_length=300, default="", blank=True)
    url = CharField(max_length=200, default="")
    status = CharField(max_length=100, default="failed", blank=True)
    instruction = TextField(default="", blank=True)

    def __str__(self):
        return self.sitename


class Product(models.Model):
    productName = CharField(max_length=100, default='', blank=True)
    instruction = TextField(blank=True)
    price = IntegerField(default=0, blank=True)
    mainPhoto = TextField(null=True)
    color = CharField(blank=False, max_length=100)
    size = TextField(null=True)
    madeOf = TextField(null=True)
    modelSize = TextField(null=True)
    review = TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.productName
