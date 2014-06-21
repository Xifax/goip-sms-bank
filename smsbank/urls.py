from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',

    # Home page
    url(r'^$', 'smsbank.views.landing', name='landing'),
    url(r'^hive/', include('smsbank.apps.hive.urls')),

    # Admin page
    url(r'^admin/', include(admin.site.urls)),
)
