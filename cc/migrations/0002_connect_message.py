# Generated by Django 3.2.4 on 2021-07-05 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Connect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_user', models.CharField(max_length=200)),
                ('reply_user', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_user', models.CharField(max_length=200)),
                ('reply_user', models.CharField(max_length=200)),
                ('message_request', models.TextField(max_length=2048)),
                ('message_reply', models.TextField(max_length=2048)),
                ('message_type', models.PositiveSmallIntegerField(choices=[(1, 'unread'), (2, 'agree'), (3, 'disagree')], default=1)),
            ],
        ),
    ]
