from django.conf.urls import patterns, url

from core.views import report, user, scheduler, examinations, api
import core.views

urlpatterns = [
    url(r'^$', core.views.user_examination_list_view, name='user_examination_list_view'),
    url(r'^(?P<user_examination_id>\d+)/$', core.views.user_examination_question_detail_view, name='user_examination_question_detail_view'),
    url(r'^(?P<user_examination_id>\d+)/(?P<question_id>\d+)/$', core.views.user_examination_question_detail_view, name='user_examination_question_detail_view'),
    url(r'^(?P<user_examination_id>\d+)/(?P<question_id>\d+)/answer/$', core.views.user_examination_answer_view, name='user_examination_answer_view'),
    url(r'^report/$', report.user_examination_report_list_view, name='user_examination_report_list_view'),
    url(r'^view/(?P<user_examination_id>\d+)/$', core.views.user_examination_detail_view, name='user_examination_detail_view'),
    url(r'^departments/$', core.views.departments_list_view, name='departments_list_view'),
    url(r'^departments/(?P<department_id>\d+)/$', core.views.department_users_list_view, name='department_users_list_view'),
    url(r'^departments/(?P<department_id>\d+)/(?P<user_id>\d+)/$', core.views.department_user_examinations_list_view, name='department_user_examinations_list_view'),

    url(r'^api/import/department/$', api.department_import, name='department_import'),
    url(r'^api/import/user/$', api.user_import, name='user_import'),

    url(r'^users/(?P<user_id>\d+)/$', user.user_create_or_update_view, name='user_update_view'),
    url(r'^users/create/$', user.user_create_or_update_view, name='user_create_view'),
    url(r'^users/$', user.user_list_view, name='user_list_view'),

    url(r'^scheduler/(?P<scheduler_id>\d+)/$', scheduler.scheduler_create_or_update_view, name='scheduler_update_view'),
    url(r'^scheduler/create/$', scheduler.scheduler_create_or_update_view, name='scheduler_create_view'),
    url(r'^scheduler/$', scheduler.scheduler_list_view, name='scheduler_list_view'),
]
