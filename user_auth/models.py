from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import NULLABLE


# Create your models here.

class User(AbstractUser):

    """
    email
    phone
    """

    username = None
    email = models.EmailField(
        unique=True,
        verbose_name='почта')
    phone = models.CharField(
        max_length=35,
        verbose_name='телефон',
        **NULLABLE)
    # chat_id = models.IntegerField(
    #     verbose_name="chat_id",
    #     **NULLABLE)
    # is_subscripted = models.BooleanField(
    #     verbose_name="Подписан",
    #     default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"


