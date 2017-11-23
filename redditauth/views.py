import praw
import json
from uuid import uuid4
import hashlib
from django.shortcuts import redirect
from django.http import HttpResponse


STATE = ''


def Reddit():
    with open('secret.json', 'r') as f:
        secret = json.load(f)

    reddit = praw.Reddit(client_id=secret['client_id'], client_secret=secret['client_secret'],
                         redirect_uri='http://localhost:8000/callback', user_agent='Plan-Reddit by /u/SkullTech101')
    return reddit


def authorize(request):
    reddit = Reddit()

    state = str(uuid4()).encode('UTF-8')
    request.session['state'] = hashlib.md5(state).hexdigest()
    request.session.modified = True

    print('printing')
    for key, value in request.session.items():
        print(key, ': ', value)
    return redirect(reddit.auth.url(['submit', 'identity'], state, 'permanent'))


def callback(request):
    print('printing')
    for key, value in request.session.items():
        print(key, ': ', value)

    error = request.GET.get('error', '')
    if error:
        return

    state = request.GET.get('state', '')
    if request.session['state'] != hashlib.md5(state.encode('UTF-8')).hexdigest():
        return

    code = request.GET.get('code', '')
    me = tokenize(code)
    return HttpResponse("Signed in as {}".format(me))


def tokenize(code):
    reddit = Reddit()
    dump = {
        'token': reddit.auth.authorize(code),
        'user': str(reddit.user.me())
    }

    with open('auth.json', 'w') as f:
        json.dump(dump, f)
    return reddit.user.me()
