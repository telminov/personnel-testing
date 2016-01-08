from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('core.views',
    url(r'^$', 'empty'),
    url(r'^exams/$', 'user_examination_list_view', name='user_examination_list_view'),
    url(r'^exams/(?P<user_exam_id>\d+)/$', 'user_examination_detail_view', name='user_examination_detail_view'),
    url(r'^exams/(?P<user_exam_id>\d+)/go/$', 'user_examination_process_view', name='user_examination_process_view'),
)
