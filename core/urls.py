from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.template.base import add_to_builtins

admin.autodiscover()
add_to_builtins('core.templatetags.core')

urlpatterns = patterns('core.views',
    url(r'^$', 'user_examination_list_view', name='user_examination_list_view'),
    url(r'^(?P<user_examination_id>\d+)/$', 'user_examination_question_detail_view', name='user_examination_question_detail_view'),
    url(r'^(?P<user_examination_id>\d+)/(?P<question_id>\d+)/$', 'user_examination_question_detail_view', name='user_examination_question_detail_view'),
    url(r'^(?P<user_examination_id>\d+)/(?P<question_id>\d+)/answer/$', 'user_examination_answer_view', name='user_examination_answer_view'),
    url(r'^view/(?P<user_examination_id>\d+)/$', 'user_examination_detail_view', name='user_examination_detail_view'),
    url(r'^report/$', 'department_users_report_list_view', name='department_users_report'),
)
