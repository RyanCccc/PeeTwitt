import json
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader, Context, Template

from pee_user.models import PeeUser
from tweet.models import Tweet, Reply, get_timestamp_str, get_timestamp

# Create your views here.
@csrf_exempt
def load_more_tweets(request):
    curr_timestamp_str = request.POST.get('timestamp_now')
    user = request.user
    try:
        my_user = PeeUser.objects.get(user=user)
        curr_timestamp = get_timestamp(curr_timestamp_str, True)
    except Exception as e:
        return return_success(False, error=e)
    followings = list(my_user.get_following())
    try:
        tweets = Tweet.objects.filter(author__in=followings, timestamp__gt=curr_timestamp).order_by('-timestamp')
        notify_count = Tweet.objects.filter(author=my_user, has_new_reply=True).count()
        if tweets:
            curr_timestamp = tweets[0].timestamp
            curr_timestamp_str = get_timestamp_str(curr_timestamp, True)
            template = Template('{% for tweet in tweets %}{% include "single_tweet.html" %}{% endfor %}')
            c = Context({
                'tweets': tweets,
                'my_user':my_user,
            })
            html = template.render(c)
            context = {
                'success':True,
                'has_new_tweets':True,
                'html':html,
                'timestamp_now':curr_timestamp_str,
                'notify_count':notify_count,
            }
            context_j = json.dumps(context)
            return HttpResponse(context_j, content_type="application/json")
        else:
            context = {
                'success':True,
                'has_new_tweets':False,
                'notify_count':notify_count,
            }
            context_j = json.dumps(context)
            return HttpResponse(context_j, content_type="application/json")
    except Exception as e:
        return return_success(False, error=e)

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
    reply_content = param.get('reply_content').strip()
    if not reply_content:
        return return_success(False)
    try:
        reply = Reply.objects.new_reply(author, tweet_pk, reply_content)
    except:
        return return_success(False)   
    if reply:
        template = loader.get_template('single_reply.html')
        c = Context({
            'reply': reply,
            'my_user':my_user,
        })
        try:
            html = template.render(c)
            context = {
                'success':True,
                'html':html,
                'tweet_pk':tweet_pk,
            }
            context_j = json.dumps(context)
            return HttpResponse(context_j, content_type="application/json")
        except:
            return return_success(False)
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
    content = param.get('content').strip()
    if not content:
        return return_success(False)
    try:
        tweet = Tweet.objects.create(author=author, content=content)
    except:
        return return_success(False)   
    if tweet:
        template = loader.get_template('single_tweet.html')
        c = Context({
            'tweet': tweet,
            'my_user':my_user,
        })
        try:
            html = template.render(c)
            context = {
                'success':True,
                'html':html,
            }
            context_j = json.dumps(context)
            return HttpResponse(context_j, content_type="application/json")
        except Exception as e:
            print e
            return return_success(False)
    else:
        return return_success(False)

def test_ajax(request):
    return render(request,'test_ajax.html')

def return_success(success=True , error=None):
    if error:
        context_j = json.dumps({'success':success,'error':str(error),})
    else:
        context_j = json.dumps({'success':success,})
    return HttpResponse(context_j, content_type="application/json")

@login_required()
def history(request):
    user = request.user
    my_user = PeeUser.objects.get(user=user)
    tweets = my_user.tweet_set.all().order_by('-timestamp')
    context = {
        'my_user':my_user,
        'tweets': tweets,
        'title':'My tweets :',
    }
    return render(request, 'home.html', context)


@login_required()
def notification(request):
    user = request.user
    my_user = PeeUser.objects.get(user=user)
    tweets = my_user.tweet_set.filter(has_new_reply=True).order_by('-timestamp')
    for tweet in tweets:
        tweet.has_new_reply = False
        tweet.save()
    context = {
        'my_user':my_user,
        'tweets': tweets,
        'title':'These tweets have new replies :',
        'no_post':True,
    }
    return render(request, 'home.html', context)

@login_required()
def profile(request, pee_user_pk):
    user = request.user
    my_user = PeeUser.objects.get(user=user)
    pee_user = PeeUser.objects.get(pk=pee_user_pk)
    is_self = False
    if my_user==pee_user:
        is_self = True
    context = {
        'my_user':my_user,
        'person':pee_user,
        'is_self':is_self,
        'tweets':pee_user.tweet_set.all().order_by('-timestamp'),
    }
    return render(request, 'user/profile.html', context)







