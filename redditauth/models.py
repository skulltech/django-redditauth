from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class AuthToken(models.Model):
    user = models.OneToOneField(User)

    token = models.CharField()
    username = models.CharField(unique=True)


def validate_reddit_username(value):
    return RegexValidator(regex='^[-_0-9a-zA-Z]{3,20}$')


class RedditUser(AbstractUser):
    username = models.CharField(unique=True, validators=[validate_reddit_username], max_length=20)
    token = models.CharField(blank=True)
    password = models.CharField(blank=True)

    USERNAME_FIELD = username
    REQUIRED_FIELDS = ['username', 'password']
