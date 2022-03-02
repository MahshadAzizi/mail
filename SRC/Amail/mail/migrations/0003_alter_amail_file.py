# Generated by Django 4.0.2 on 2022-03-02 18:15

from django.db import migrations, models
import mail.models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0002_amail_is_read'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amail',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='documents/', validators=[mail.models.file_size]),
        ),
    ]