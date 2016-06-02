from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest

import re
from datetime import timedelta
import json
import tweepy

from .models import Greeting

def index(request):
    return render(request, 'index.html')


def tweets(request):
    screen_name = request.GET.get('screen_name')
    if not re.search(r'^\w+$', screen_name):
        return HttpResponseBadRequest()

    consumer_key="A6fiN33tLablelq9pfgbILvfT"
    consumer_secret="MlfSrZem0iSg1Ku7L2nadF01XzwgPlWG5090Ww9Y1lPrWHkPMu"
    access_token="933582354-t0VlfS295q3kTvCuDvz0OTXTJuk8Lax5vb73vPDN"
    access_token_secret="7l1Hq2vPWwFpAmEiOReQ06zJa0AoZRqKTUXRYWvCy6dSU"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name=screen_name, count=200)
    stat = [[0 for j in xrange(24)] for i in xrange(7)]
    for tweet in tweets:
        ts = tweet.created_at
        ts += timedelta(hours=+9)
        stat[ts.weekday()][ts.hour] += 1

    delta = tweets[0].created_at - tweets[-1].created_at
    speed = len(tweets) * (24.0*60*60) / delta.total_seconds()
    response = {'data': [], 'speed': "%.2f" % speed}
    for day, v in enumerate(stat):
        for hour, count in enumerate(v):
            response['data'].append({'day': day+1, 'hour': hour, 'value': count})

    return HttpResponse(json.dumps(response), content_type='application/json')
