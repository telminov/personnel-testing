from django.conf.urls import patterns, url

import core.views

urlpatterns = [
    url(r'^$', core.views.user_examination_list_view, name='user_examination_list_view'),
    url(r'^(?P<user_examination_id>\d+)/$', core.views.user_examination_question_detail_view, name='user_examination_question_detail_view'),
    url(r'^(?P<user_examination_id>\d+)/(?P<question_id>\d+)/$', core.views.user_examination_question_detail_view, name='user_examination_question_detail_view'),
    url(r'^(?P<user_examination_id>\d+)/(?P<question_id>\d+)/answer/$', core.views.user_examination_answer_view, name='user_examination_answer_view'),
    url(r'^report/$', core.views.user_examination_report_list_view, name='user_examination_report_list_view'),
    url(r'^view/(?P<user_examination_id>\d+)/$', core.views.user_examination_detail_view, name='user_examination_detail_view'),
    url(r'^departments/$', core.views.departments_list_view, name='departments_list_view'),
    url(r'^departments/(?P<department_id>\d+)/$', core.views.department_users_list_view, name='department_users_list_view'),
    url(r'^departments/(?P<department_id>\d+)/(?P<user_id>\d+)/$', core.views.department_user_examinations_list_view, name='department_user_examinations_list_view'),
]
