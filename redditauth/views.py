import praw
import json
from uuid import uuid4
import hashlib
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required



def authorize(request):
    with open('secret.json', 'r') as f:
        secret = json.load(f)

    reddit = praw.Reddit(client_id=secret['client_id'], client_secret=secret['client_secret'],
                         redirect_uri='http://localhost:8000/callback', user_agent='Plan-Reddit by /u/SkullTech101')

    state = str(uuid4()).encode('UTF-8')
    request.session['state'] = hashlib.md5(state).hexdigest()
    request.session.modified = True

    return redirect(reddit.auth.url(['submit', 'identity'], state, 'permanent'))


def callback(request):
    error = request.GET.get('error', '')
    if error:
        return

    state = request.GET.get('state', '')
    if request.session['state'] != hashlib.md5(state.encode('UTF-8')).hexdigest():
        return

    code = request.GET.get('code', '')
    user = authenticate(request=request, code=code)
    login(request, user)
    return HttpResponse("Signed in as {}".format(user.username))


@login_required(login_url='/authorize')
def home(request):
    return HttpResponse("Signed in as {}".format(request.user.username))
