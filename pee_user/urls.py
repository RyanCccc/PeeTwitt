from django.conf.urls import patterns, include, url

urlpatterns = patterns('pee_user.views',
    url(r'^signup/$', 'signup', name='pee_user_signup'),
)
