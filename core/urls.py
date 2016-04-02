from django.conf.urls import patterns, url

from core.views import report, user, scheduler, examinations, api, user_examinations, department, examination

urlpatterns = [
    url(r'^$', examination.user_examination_list_view, name='user_examination_list_view'),
    url(r'^(?P<user_examination_id>\d+)/$', examination.user_examination_process_view, name='user_examination_question_detail_view'),
    url(r'^(?P<user_examination_id>\d+)/(?P<user_examination_question_log_id>\d+)/$', examination.user_examination_process_view, name='user_examination_question_detail_view'),
    url(r'^(?P<user_examination_id>\d+)/(?P<user_examination_question_log_id>\d+)/$', examination.user_examination_process_view, name='user_examination_answer_view'),
    url(r'^view/(?P<user_examination_id>\d+)/$', examination.user_examination_detail_view, name='user_examination_detail_view'),

    url(r'^report/$', report.user_examination_report_list_view, name='user_examination_report_list_view'),

    url(r'^departments/$', department.departments_list_view, name='departments_list_view'),
    url(r'^departments/(?P<department_id>\d+)/$', department.department_users_list_view, name='department_users_list_view'),
    url(r'^departments/(?P<department_id>\d+)/(?P<user_id>\d+)/$', department.department_user_examinations_list_view, name='department_user_examinations_list_view'),

    url(r'^api/import/department/$', api.department_import, name='department_import'),
    url(r'^api/import/user/$', api.user_import, name='user_import'),

    url(r'^users/(?P<user_id>\d+)/$', user.user_create_or_update_view, name='user_update_view'),
    url(r'^users/create/$', user.user_create_or_update_view, name='user_create_view'),
    url(r'^users/$', user.user_list_view, name='user_list_view'),

    url(r'^scheduler/(?P<scheduler_id>\d+)/detail/$', scheduler.scheduler_detail_view, name='scheduler_detail_view'),
    url(r'^scheduler/(?P<scheduler_id>\d+)/$', scheduler.scheduler_create_or_update_view, name='scheduler_update_view'),
    url(r'^scheduler/create/$', scheduler.scheduler_create_or_update_view, name='scheduler_create_view'),
    url(r'^scheduler/$', scheduler.scheduler_list_view, name='scheduler_list_view'),

    url(r'^examination/(?P<examination_id>\d+)/$', examinations.examination_create_or_update_view, name='examination_update_view'),
    url(r'^examination/create/$', examinations.examination_create_or_update_view, name='examination_create_view'),
    url(r'^examination/$', examinations.examination_list_view, name='examination_list_view'),

    url(r'^user_examination/(?P<user_examination_id>\d+)/$', user_examinations.user_examination_create_or_update_view, name='user_examination_update_view'),
    url(r'^user_examination/create/$', user_examinations.user_examination_create_or_update_view, name='user_examination_create_view'),
    url(r'^user_examination/$', user_examinations.user_examination_list_view, name='user_examination_list_view'),
]
