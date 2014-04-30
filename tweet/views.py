import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from pee_user.models import PeeUser
from tweet.models import Tweet, Reply

# Create your views here.
@csrf_exempt
def load_more_tweets(request):
    curr_pk = request.POST.get('curr_pk')
    user = request.user
    try:
        my_user = PeeUser.objects.get(user=user)
    except:
        return return_success(False)
    followings = list(my_user.followings.all())
    followings.append(my_user)
    tweets = Tweet.objects.filter(author__in=followings, pk__gt=curr_pk).order_by('-timestamp')
    if tweets:
        curr_pk = tweets[0].pk
    print 'Hello'
    tweets_obj = []    
    for tweet in tweets:
        tweet_obj = {
            'author': tweet.author.full_name(),
            'content': tweet.content,
            'timestamp': str(tweet.timestamp),
        }
        tweets_obj.append(tweet_obj)
    notify_count = Tweet.objects.filter(author=my_user, has_new_reply=True).count()
    context = {
        'success':True,
        'tweets':tweets_obj,
        'curr_pk':curr_pk,
        'notify_count':notify_count,
    }
    context_j = json.dumps(context)
    return HttpResponse(context_j, content_type="application/json")

@csrf_exempt
def reply(request):
    user = request.user
    try:
        my_user = PeeUser.objects.get(user=user)
    except:
        return return_success(False)
    author = my_user
    param = request.POST
    tweet_pk = param.get('tweet_pk')
    reply_content = param.get('reply_content')
    try:
        reply = Reply.objects.new_reply(author, tweet_pk, reply_content)
    except:
        return return_success(False)   
    if reply:
        return return_success()
    else:
        return return_success(False)

@csrf_exempt
def post_tweet(request):
    user = request.user
    try:
        my_user = PeeUser.objects.get(user=user)
    except:
        return return_success(False)
    author = my_user
    param = request.POST
    content = param.get('content')
    try:
        tweet = Tweet.objects.create(author=author, content=content)
    except:
        return return_success(False)   
    if tweet:
        return return_success()
    else:
        return return_success(False)

def test_ajax(request):
    return render(request,'test_ajax.html')

def return_success(success=True):
    context_j = json.dumps({'success':success,})
    return HttpResponse(context_j, content_type="application/json")