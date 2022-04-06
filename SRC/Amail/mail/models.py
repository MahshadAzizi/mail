from django.core.exceptions import ValidationError
from django.db import models
from user.models import User, Signature
from ckeditor_uploader.fields import RichTextUploadingField

STATUS = [
    ('draft', 'draft'),
    ('send', 'send')
]


def file_size(file):
    limit = 262014400
    if file.size > limit:
        raise ValidationError('File too large. Size should not exceed 25 mb.')


class Filter(models.Model):
    CATEGORY_CHOICES = (
        ('no', '----'),
        ('label', 'LABEL'),
        ('trash', 'TRASH'),
        ('archive', 'ARCHIVE')
    )
    sender = models.CharField(max_length=50, blank=True, null=True, help_text=('username@Amail.com'))
    subject = models.CharField(max_length=500, blank=True, null=True)
    body = models.TextField(max_length=500, blank=True, null=True)
    file = models.BooleanField(default=False, blank=True, null=True)
    action = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='no')


class Category(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Amail(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='amail_sender')
    receiver = models.ManyToManyField(User, related_name='amail_receiver')
    bcc = models.ManyToManyField(User, related_name='bcc', blank=True)
    cc = models.ManyToManyField(User, related_name='cc', blank=True)
    subject = models.CharField(max_length=80, null=True, blank=True)
    # body = models.TextField(max_length=255, null=True, blank=True)
    body = RichTextUploadingField(null=True, blank=True)
    mail_date = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category, blank=True)
    archive = models.BooleanField(null=True, default=False)
    file = models.FileField(validators=[file_size], null=True, upload_to='documents/', blank=True)
    signature = models.ForeignKey(Signature, on_delete=models.DO_NOTHING, null=True, blank=True)
    trash = models.BooleanField(null=True, default=False)
    reply = models.ManyToManyField('Amail')
    status = models.CharField(max_length=5, choices=STATUS, null=True)
    filter = models.ManyToManyField(Filter, blank=True)
    is_read = models.BooleanField(default=False)

    @property
    def file_size(self):
        if self.file and hasattr(self.file, 'size'):
            return self.file.size

    def __str__(self):
        return str(self.sender) + " - " + str(self.subject)
