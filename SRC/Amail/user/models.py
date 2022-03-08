import re
from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

RECOVERY = [
    ('phone', 'phone'),
    ('email', 'email')
]

GENDER = [
    ('F', 'female'),
    ('M', 'male'),
    ('O', 'other')
]


def user_validator(username):
    match = re.search('@Amail.com', username)
    if match:
        raise ValidationError('You should not use @Amail.com')


class User(AbstractUser):
    username = models.CharField(validators=[user_validator], max_length=30, unique=True)
    recovery = models.CharField(choices=RECOVERY, max_length=15, null=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER, null=True, blank=True)
    birth_date = models.DateTimeField(null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.crew_password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {} - {}".format(self.phone_number, self.code, self.created)


class ContactBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
