# Generated by Django 4.0.2 on 2022-03-03 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0003_alter_amail_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='amail',
            name='reply',
        ),
        migrations.AddField(
            model_name='amail',
            name='reply',
            field=models.ManyToManyField(to='mail.Amail'),
        ),
    ]