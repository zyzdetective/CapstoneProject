from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_type1 = models.BooleanField(default=False)
    is_type2 = models.BooleanField(default=False)

    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)

class User_Type_1(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user_type_1_teyoushuxing = models.CharField(max_length=200)

    class Meta:
        db_table = 'charity'
        verbose_name = 'charity'
        verbose_name_plural = verbose_name

class User_Type_2(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user_type_2_teyoushuxing = models.CharField(max_length=200)

    class Meta:
        db_table = 'sponsor'
        verbose_name = 'sponsor'
        verbose_name_plural = verbose_name
