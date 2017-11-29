from django.db import models
import praw
import json
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
    username = models.CharField(unique=True, primary_key=True, validators=[validate_reddit_username], max_length=20)
    token = models.CharField()

    USERNAME_FIELD = username
    REQUIRED_FIELDS = ['username', 'token']

    def reddit(self):
        with open('secret.json', 'r') as f:
            secret = json.load(f)

        return praw.Reddit(client_id=secret['client_id'], client_secret=secret['client_secret'],
                             refresh_token=self.token, user_agent='Plan-Reddit by /u/SkullTech101')


