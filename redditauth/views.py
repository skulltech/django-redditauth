import praw
import json
from uuid import uuid4
import hashlib
from django.shortcuts import redirect

STATE = ''


def Reddit():
    with open('secret.json', 'r') as f:
        secret = json.load(f)

    reddit = praw.Reddit(client_id=secret['client_id'], client_secret=secret['client_secret'],
                         redirect_uri='http://localhost:8000/callback', user_agent='Plan-Reddit by /u/SkullTech101')
    return reddit


def authorize(request):
    reddit = Reddit()

    state = uuid4()
    request.session['state'] = hashlib.md5(state).hexdigest()
    return redirect(reddit.auth.url(['submit'], state, 'permanent'))


def callback(request):
    error = request.GET.get('error', '')
    if error:
        return

    state = request.GET.get('state', '')
    if request.session['state'] != hashlib.md5(state).hexdigest():
        return

    code = request.GET.get('code', '')
    tokenize(code)


def tokenize(code):
    reddit = Reddit()
    dump = {
        'token': reddit.auth.authorize(code),
        'user': reddit.user.me()
    }

    with open('auth.json', 'w') as f:
        json.dump(dump, f)
