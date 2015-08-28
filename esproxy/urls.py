from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from settings import AUTHENTICATION_BACKENDS
if 'django_cas.backends.CASBackend' in AUTHENTICATION_BACKENDS:
    from django_cas.views import login,logout
else:
    from esproxy import login,logout

urlpatterns = patterns(
    '',
    url(r'^$', 'esproxy.views.home'),
    url(r'^index.html', 'esproxy.views.index'),
    url(r'^elasticsearch/', 'esproxy.views.elasticsearch'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login.html$', csrf_exempt(login)),
    url(r'^logout.html$',logout),
)
