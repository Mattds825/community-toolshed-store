# Generated by Django 5.1.4 on 2025-03-17 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_userprofile_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email_address',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
