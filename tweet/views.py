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
    followings = list(my_user.get_following())
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
            'timestamp': tweet.get_timestamp_str(),
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
    reply_content = param.get('reply_content').strip()
    if not reply_content:
        return return_success(False)
    try:
        reply = Reply.objects.new_reply(author, tweet_pk, reply_content)
    except:
        return return_success(False)   
    if reply:
        html = """
        <div style="border-top: 1px solid #C9C9C9;">
            <div class="col-xs-2" style="width:18%;">
                <a href="#">
                <img class="avatartweetpic" onload="" style="max-height:40px;max-width:40px;" src="{0}">
                </a>
            </div>

            <div class="post-right">
                <div>
                    <span><b>{1}</b>
                    </span>
                    at <span>{2}</span>
                    <br>
                    <span>{3}</span>
                </div>
            </div>
        </div>
        <br>
        """
        try:
            html = html.format(my_user.get_img_url(), my_user.full_name(), reply.get_timestamp_str(), reply.content)
            context = {
                'success':True,
                'html':html,
                'tweet_pk':tweet_pk,
            }
            context_j = json.dumps(context)
            return HttpResponse(context_j, content_type="application/json")
        except Exception as e:
            print e
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
        html = """
        <div class="row no-gutter post" tweet_pk="{0}">
                    <!--post#1-->


                    <div class="col-md-12">
                        <div class="col-md-3" style="width:20%;">
                            <a href="#">
                                <img class="avatartweetpic" onload="" src="{1}">
                            </a>
                        </div>

                        <div class="col-md-9" style="padding-left:0px">
                            <div class="post-right">
                                <div class="tweet">
                                    <span ><b id="tweet_author_name">{2}</b>
                                    </span>
                                    at
                                    <span id="tweet_timestamp">{3}</span>
                                    <br>
                                    <span id="tweet_content">{4}</span>
                                </div>

                                <div class="comments">
                                    
                                </div>
                            </div>


                        </div>

                        <div class="col-md-12 reply">
                            <div class="reply2">
                                <div class="col-xs-3" style="width:18%;">
                                    <a href="#">
                                        <img class="avatartweetpic" onload="" style="max-height:50px;max-width:50px;" src="{5}">
                                    </a>
                                </div>

                                <div class="col-xs-9 post-right">
                                    <input type="text" class="form-control" name="reply" placeholder="Reply...">
                                    <button type="button" class="btn btn-primary btn-xs btnReply" name='button' value='reply' tweet_pk="{6}">reply</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                """
        try:
            html = html.format(tweet.pk, my_user.get_img_url(), my_user.full_name(), tweet.get_timestamp_str(), tweet.content, my_user.get_img_url(), tweet.pk)
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

def return_success(success=True):
    context_j = json.dumps({'success':success,})
    return HttpResponse(context_j, content_type="application/json")