# Generated by Django 3.2.4 on 2021-07-08 04:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cc', '0002_connect_message'),
    ]

    operations = [
        migrations.RenameField(
            model_name='connect',
            old_name='reply_user',
            new_name='charity_user',
        ),
        migrations.RenameField(
            model_name='connect',
            old_name='request_user',
            new_name='sponsor_user',
        ),
    ]
