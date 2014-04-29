import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from pee_user.models import PeeUser
from tweet.models import Tweet

# Create your views here.
@csrf_exempt
def load_more_tweets(request):
    curr_pk = request.POST.get('curr_pk')
    user = request.user
    my_user = PeeUser.objects.get(user=user)
    last_tweet = Tweet.objects.get(pk=curr_pk)
    last_time = last_tweet.timestamp
    tweets = []
    for tweet in Tweet.objects.filter(timestamp__lt=last_time).order_by('-timestamp'):
        if tweet.author in my_user.followings:
            tweets.append(tweet)
            if len(tweets)>=10:
                break
    context = []
    for tweet in tweets:
        tweet_json = {
            'author': tweet.author.first_name + ' ' + tweet.author.last_name,
            'content': tweet.content,
            'timestamp': str(tweet),
        }
        context.append(tweet_json)
    context_j = json.dumps(context)
    return HttpResponse(context_j, content_type="application/json")