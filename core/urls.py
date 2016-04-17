from django.conf.urls import patterns, url

from core.views import report, user, scheduler, examinations, api, user_examinations, department, examination, doc
from core.views.management import department

urlpatterns = [
    url(r'^$', examination.user_examination_list_view, name='user_examination_list_view'),
    url(r'^(?P<user_examination_id>\d+)/$', examination.user_examination_process_view, name='user_examination_answer_view'),
    url(r'^(?P<user_examination_id>\d+)/(?P<user_examination_question_log_id>\d+)/$', examination.user_examination_process_view, name='user_examination_answer_view'),
    url(r'^view/(?P<user_examination_id>\d+)/$', examination.user_examination_detail_view, name='user_examination_detail_view'),

    # url(r'^api/import/department/$', api.department_import, name='department_import'),
    # url(r'^api/import/user/$', api.user_import, name='user_import'),

    url(r'^adm/report/$', report.user_examination_report_list_view, name='user_examination_report_list_view'),

    url(r'^adm/departments/$', report.departments_report_list_view, name='departments_report_list_view'),
    url(r'^adm/departments/(?P<department_id>\d+)/$', report.department_users_list_view, name='department_users_list_view'),
    url(r'^adm/departments/(?P<department_id>\d+)/(?P<user_id>\d+)/$', report.department_user_examinations_list_view, name='department_user_examinations_list_view'),

    url(r'^adm/users/(?P<user_id>\d+)/delete/$', user.user_delete_view, name='user_delete_view'),
    url(r'^adm/users/(?P<user_id>\d+)/$', user.user_create_or_update_view, name='user_update_view'),
    url(r'^adm/users/create/$', user.user_create_or_update_view, name='user_create_view'),
    url(r'^adm/users/deleted/$', user.user_deleted_list_view, name='user_deleted_list_view'),
    url(r'^adm/users/$', user.user_list_view, name='user_list_view'),

    url(r'^adm/scheduler/(?P<scheduler_id>\d+)/detail/$', scheduler.scheduler_detail_view, name='scheduler_detail_view'),
    url(r'^adm/scheduler/(?P<scheduler_id>\d+)/$', scheduler.scheduler_create_or_update_view, name='scheduler_update_view'),
    url(r'^adm/scheduler/create/$', scheduler.scheduler_create_or_update_view, name='scheduler_create_view'),
    url(r'^adm/scheduler/$', scheduler.scheduler_list_view, name='scheduler_list_view'),

    url(r'^adm/examination/(?P<examination_id>\d+)/questions/(?P<question_id>\d+)/answer/(?P<answer_id>\d+)/delete/$', examinations.question_answer_delete_view, name='question_answer_delete_view'),
    url(r'^adm/examination/(?P<examination_id>\d+)/questions/(?P<question_id>\d+)/answer/(?P<answer_id>\d+)/$', examinations.question_answer_create_or_update_view, name='question_answer_update_view'),
    url(r'^adm/examination/(?P<examination_id>\d+)/questions/(?P<question_id>\d+)/answer/create/$', examinations.question_answer_create_or_update_view, name='question_answer_create_view'),
    url(r'^adm/examination/(?P<examination_id>\d+)/questions/(?P<question_id>\d+)/delete/$', examinations.examination_question_delete_view, name='examination_question_delete_view'),
    url(r'^adm/examination/(?P<examination_id>\d+)/questions/(?P<question_id>\d+)/$', examinations.examination_question_create_or_update_view, name='examination_question_update_view'),
    url(r'^adm/examination/(?P<examination_id>\d+)/questions/create/$', examinations.examination_question_create_or_update_view, name='examination_question_create_view'),
    url(r'^adm/examination/(?P<examination_id>\d+)/questions/$', examinations.examination_question_list_view, name='examination_question_list_view'),
    url(r'^adm/examination/(?P<examination_id>\d+)/delete/$', examinations.examination_delete_view, name='examination_delete_view'),
    url(r'^adm/examination/(?P<examination_id>\d+)/$', examinations.examination_create_or_update_view, name='examination_update_view'),
    url(r'^adm/examination/create/$', examinations.examination_create_or_update_view, name='examination_create_view'),
    url(r'^adm/examination/deleted/$', examinations.examination_deleted_list_view, name='examination_deleted_list_view'),
    url(r'^adm/examination/$', examinations.examination_list_view, name='adm_examination_list_view'),

    url(r'^adm/user_examination/(?P<user_examination_id>\d+)/$', user_examinations.user_examination_create_or_update_view, name='adm_user_examination_update_view'),
    url(r'^adm/user_examination/create/$', user_examinations.user_examination_create_or_update_view, name='adm_user_examination_create_view'),
    url(r'^adm/user_examination/$', user_examinations.user_examination_list_view, name='adm_user_examination_list_view'),

    url(r'^adm/department/(?P<department_id>\d+)/$', department.department_create_or_update_view, name='department_update_view'),
    url(r'^adm/department/create/$', department.department_create_or_update_view, name='department_create_view'),
    url(r'^adm/department/$', department.department_list_view, name='department_list_view'),
]
