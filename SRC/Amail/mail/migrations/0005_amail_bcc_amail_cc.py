# Generated by Django 4.0.2 on 2022-03-05 11:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mail', '0004_remove_amail_reply_amail_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='amail',
            name='bcc',
            field=models.ManyToManyField(related_name='bcc', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='amail',
            name='cc',
            field=models.ManyToManyField(related_name='cc', to=settings.AUTH_USER_MODEL),
        ),
    ]