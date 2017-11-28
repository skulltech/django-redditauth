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
    token = models.CharField(blank=True)
    password = models.CharField(blank=True)

    USERNAME_FIELD = username
    REQUIRED_FIELDS = ['username', 'password']


class RedditBackend:
    @staticmethod
    def authenticate(request, username=None, password=None, code=None):
        try:
            user = RedditUser.objects.get(username=username)
        except RedditUser.DoesNotExist:
            if code:
                with open('secret.json', 'r') as f:
                    secret = json.load(f)

                reddit = praw.Reddit(client_id=secret['client_id'], client_secret=secret['client_secret'],
                                     redirect_uri='http://localhost:8000/callback',
                                     user_agent='Plan-Reddit by /u/SkullTech101')
                token = reddit.auth.authorize(code)
                user = RedditUser(username=reddit.user.me(), token=token)
                return user
            else:
                user = RedditUser(username=username, password=password)
                return user

    @staticmethod
    def get_user(username):
        try:
            RedditUser.objects.get(username=username)
        except RedditUser.DoesNotExist:
            return None
