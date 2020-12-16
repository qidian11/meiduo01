from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):

    moblie = models.CharField(verbose_name='手机号',max_length=11,unique=True)

    class Meta:
        db_table = 'tb_users'