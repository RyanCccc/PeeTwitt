from django.conf.urls import patterns, include, url

urlpatterns = patterns('tweet.views',
    url(r'^load_more_tweets/$', 'load_more_tweets', name='tweet_load_more_tweets'),
    url(r'^reply/$', 'reply', name='tweet_reply'),
    url(r'^post_tweet/$', 'post_tweet', name='tweet_post_tweet'),
    url(r'^test_ajax/$', 'test_ajax', name='tweet_test_ajax'),
    url(r'^history/$', 'history', name='tweet_history'),
    url(r'^notification/$', 'notification', name='tweet_notification'),
    url(r'^([0-9]+)/$', 'profile', name='tweet_profile'),
)