from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('PeeTwitt.views',
    # Examples:
    # url(r'^$', 'PeeTwitt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'index', name='index'),
    url(r'^home/$', 'home', name='home'),
    url(r'^t/', include('tweet.urls')),
    url(r'^account/', include('pee_user.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)