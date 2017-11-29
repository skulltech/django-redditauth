import json
import praw
from .models import RedditUser


class RedditBackend:
    @staticmethod
    def authenticate(request, username=None, code=None):
        try:
            return RedditUser.objects.get(username=username)
        except RedditUser.DoesNotExist:
            if code:
                with open('secret.json', 'r') as f:
                    secret = json.load(f)
                reddit = praw.Reddit(client_id=secret['client_id'], client_secret=secret['client_secret'],
                                     redirect_uri='http://localhost:8000/callback',
                                     user_agent='Plan-Reddit by /u/SkullTech101')
                token = reddit.auth.authorize(code)
                return RedditUser(username=reddit.user.me(), token=token)

        return None

    @staticmethod
    def get_user(username):
        try:
            return RedditUser.objects.get(username=username)
        except RedditUser.DoesNotExist:
            return None
