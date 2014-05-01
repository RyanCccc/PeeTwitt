from django.conf.urls import patterns, include, url

urlpatterns = patterns('pee_user.views',
    url(r'^signup/$', 'signup', name='pee_user_signup'),
    url(r'^verify/$', 'verify', name='pee_user_verify'),
    url(r'^signin/$', 'signin', name='pee_user_signin'),
    url(r'^resend/$', 'resend', name='pee_user_resend'),
    url(r'^signout/$', 'signout', name='pee_user_signout'),
    url(r'^search/$', 'search', name='pee_user_search'),
    url(r'^follow/$', 'follow', name='pee_user_follow'),
    url(r'^unfollow/$', 'unfollow', name='pee_user_unfollow'),
)