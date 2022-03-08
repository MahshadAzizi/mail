from django.core.exceptions import ValidationError
from django.db import models
from user.models import User

STATUS = [
    ('draft', 'draft'),
    ('send', 'send')
]


def file_size(file):
    limit = 262014400
    if file.size > limit:
        raise ValidationError('File too large. Size should not exceed 25 mb.')


class Category(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Amail(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='amail_sender')
    receiver = models.ManyToManyField(User, related_name='amail_receiver')
    bcc = models.ManyToManyField(User, related_name='bcc')
    cc = models.ManyToManyField(User, related_name='cc')
    subject = models.CharField(max_length=80, null=True, blank=True)
    body = models.TextField(max_length=255, null=True, blank=True)
    mail_date = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category)
    archive = models.BooleanField(null=True, default=False)
    file = models.FileField(validators=[file_size], null=True, upload_to='documents/', blank=True)
    signature = models.TextField(max_length=255, null=True, blank=True)
    trash = models.BooleanField(null=True, default=False)
    reply = models.ManyToManyField('Amail')
    status = models.CharField(max_length=5, choices=STATUS, null=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return str(self.sender) + " - " + str(self.subject)
