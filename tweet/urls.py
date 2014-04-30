from django.conf.urls import patterns, include, url

urlpatterns = patterns('tweet.views',
    url(r'^load_more_tweets/$', 'load_more_tweets', name='tweet_load_more_tweets'),
    url(r'^reply/$', 'reply', name='tweet_reply'),
    url(r'^post_tweet/$', 'post_tweet', name='tweet_post_tweet'),
    url(r'^test_ajax/$', 'test_ajax', name='tweet_test_ajax')
)