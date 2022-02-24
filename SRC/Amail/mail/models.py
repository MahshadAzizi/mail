from django.core.exceptions import ValidationError
from django.db import models
from user.models import User


def file_size(file):
    limit = 262014400
    if file.size > limit:
        raise ValidationError('File too large. Size should not exceed 25 mb.')


class Category(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Signature(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=100, null=True)

    def __str__(self):
        return self.text


class Amail(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='amail_sender')
    reciever = models.ManyToManyField(User, related_name='amail_reciever')
    subject = models.CharField(max_length=80, null=True, blank=True)
    body = models.TextField(max_length=255, null=True, blank=True)
    mail_date = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category, related_name='amail_category')
    archive = models.BooleanField(null=True, default=False)
    file = models.FileField(validators=[file_size], null=True, upload_to='media/', blank=True)
    signature = models.ForeignKey(Signature, on_delete=models.DO_NOTHING, null=True, blank=True)
    trash = models.BooleanField(null=True, default=False)
    replay = models.ForeignKey('Amail', on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.sender, self.subject
