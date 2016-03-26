# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin


from .models import User, Department, Examination, Question, Answer, UserExamination,\
    UserExaminationQuestionLog, UserExaminationAnswerLog, Scheduler


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', )


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', )


class ExaminationAdmin(admin.ModelAdmin):
    list_display = ('name', 'department',)


class AnswerInline(admin.StackedInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('body', )

    inlines = [
        AnswerInline
    ]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('body', )


class UserExaminationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'examination', )


class UserExaminationAnswerAdmin(admin.ModelAdmin):
    list_display = ('user_examination', )


class UserExaminationQuestionLogAdmin(admin.ModelAdmin):
    pass


class UserExaminationAnswerLogAdmin(admin.ModelAdmin):
    pass


class SchedulerAdmin(admin.ModelAdmin):
    list_display = ('examination', 'count', 'period', 'unit')


admin.site.register(User, UserAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Examination, ExaminationAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(UserExamination, UserExaminationAdmin)
admin.site.register(UserExaminationQuestionLog, UserExaminationQuestionLogAdmin)
admin.site.register(UserExaminationAnswerLog, UserExaminationAnswerLogAdmin)
admin.site.register(Scheduler, SchedulerAdmin)
