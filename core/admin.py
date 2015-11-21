# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from mptt.admin import MPTTModelAdmin


from .models import User, Organization, Department, Examination, Question, Answer, UserExamination, UserExaminationAnswer


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'director', )


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', )


class DepartmentAdmin(MPTTModelAdmin):
    list_display = ('name', 'responsible', )


class ExaminationAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'started_at', 'finished_at')
    list_filter = ('started_at', 'finished_at')


class AnswerInline(admin.StackedInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name', )

    inlines = [
        AnswerInline
    ]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('name', )


class UserExaminationAdmin(admin.ModelAdmin):
    list_display = ('examination', )


class UserExaminationAnswerAdmin(admin.ModelAdmin):
    list_display = ('user_examination', )


admin.site.register(User, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Examination, ExaminationAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(UserExamination, UserExaminationAdmin)
admin.site.register(UserExaminationAnswer, UserExaminationAnswerAdmin)
