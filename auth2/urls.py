from django.conf.urls import patterns, include, url
from django.contrib import admin

import auth2.views

admin.autodiscover()

urlpatterns = [
    url(r'^login/$', auth2.views.login, name='login'),
    url(r'^logout/$', auth2.views.logout, name='logout'),
]
