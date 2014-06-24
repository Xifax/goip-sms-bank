from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',

    # Landing
    url(r'^$', views.index, name='index'),

    # Working with devices
    url(r'^grunts/', views.grunts, name='grunts'),
    url(
        r'^grunt/list/(?P<grunt>[0-9]+)/',
        views.grunt_list, name='grunt-list'
        ),
    url(
        r'^grunt/send/(?P<grunt>[0-9]+)/',
        views.grunt_send, name='grunt-send'
        ),

    # Profile
    url(r'^profile/', views.profile, name='profile'),

    # Additional
    url(r'^info/', views.info, name='info'),

    # Auth
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^logout/', views.logout, name='logout'),
)
