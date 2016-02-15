from django.conf.urls import patterns, url

import core.views

urlpatterns = [
    url(r'^$', core.views.user_examination_list_view, name='user_examination_list_view'),
    url(r'^(?P<user_examination_id>\d+)/$', core.views.user_examination_question_detail_view, name='user_examination_question_detail_view'),
    url(r'^(?P<user_examination_id>\d+)/(?P<question_id>\d+)/$', core.views.user_examination_question_detail_view, name='user_examination_question_detail_view'),
    url(r'^(?P<user_examination_id>\d+)/(?P<question_id>\d+)/answer/$', core.views.user_examination_answer_view, name='user_examination_answer_view'),
    url(r'^view/(?P<user_examination_id>\d+)/$', core.views.user_examination_detail_view, name='user_examination_detail_view'),
    url(r'^report/$', core.views.department_users_report_list_view, name='department_users_report'),
]
