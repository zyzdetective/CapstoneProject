from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    email = models.EmailField(
        blank=True,
        unique=True,
        error_messages={
            'unique': "A user with that email already exists.",
        }
    )
    USER_TYPE_CHOICES = (
        (1, 'charity'),
        (2, 'sponsor'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)


class UserCharity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=200)
    long_name = models.CharField(max_length=200)
    description = models.CharField(max_length=2048)
    email = models.EmailField(
        blank=True,
        unique=True,
        error_messages={
            'unique': "A user with that email already exists.",
        }
    )
    website = models.URLField()

    class Meta:
        db_table = 'charity'
        verbose_name = 'charity'
        verbose_name_plural = verbose_name


class UserSponsor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=200)
    long_name = models.CharField(max_length=200)
    description = models.CharField(max_length=2048)
    email = models.EmailField(
        blank=True,
        unique=True,
        error_messages={
            'unique': "A user with that email already exists.",
        }
    )
    website = models.URLField()

    class Meta:
        db_table = 'sponsor'
        verbose_name = 'sponsor'
        verbose_name_plural = verbose_name


class Need(models.Model):
    username = models.ForeignKey('User', to_field='username', on_delete=models.CASCADE)
    # this variety need should not be changed due to \ref { views.py 103 }
    need = models.CharField(max_length=200)


class Provide(models.Model):
    username = models.ForeignKey('User', to_field='username', on_delete=models.CASCADE)
    # this variety need should not be changed due to \ref { views.py 103 }
    need = models.CharField(max_length=200)


class Message(models.Model):
    request_user = models.CharField(max_length=200)
    reply_user = models.CharField(max_length=200)
    message_request = models.TextField(max_length=2048)
    message_reply = models.TextField(max_length=2048)

    MESSAGE_TYPE_CHOICES = (
        (1, 'unread'),
        (2, 'agree'),
        (3, 'disagree'),
    )
    message_type = models.PositiveSmallIntegerField(choices=MESSAGE_TYPE_CHOICES, default=1)


class Connect(models.Model):
    charity_user = models.CharField(max_length=200)
    sponsor_user = models.CharField(max_length=200)
