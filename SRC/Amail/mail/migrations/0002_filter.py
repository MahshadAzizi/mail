# Generated by Django 4.0.2 on 2022-04-04 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(blank=True, help_text='username@Amail.com', max_length=50, null=True)),
                ('subject', models.CharField(blank=True, max_length=500, null=True)),
                ('body', models.TextField(blank=True, max_length=500, null=True)),
                ('file', models.BooleanField(blank=True, default=False, null=True)),
                ('action', models.CharField(choices=[('no', '----'), ('label', 'LABEL'), ('trash', 'TRASH'), ('archive', 'ARCHIVE')], default='no', max_length=20)),
            ],
        ),
    ]
