from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('PeeTwitt.views',
    # Examples:
    # url(r'^$', 'PeeTwitt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'index', name='index'),
    url(r'^home/$', 'home', name='home'),
    url(r'^r/', include('tweet.urls')),
    url(r'^account/', include('pee_user.urls')),
)
