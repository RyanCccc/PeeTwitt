from django.conf.urls import patterns, include, url

urlpatterns = patterns('tweet.views',
    url(r'^load_more_tweets/$', 'load_more_tweets', name='tweet_load_more_tweets'),
)