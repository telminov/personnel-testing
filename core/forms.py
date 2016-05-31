# coding: utf-8
from django import forms

from django_select2.forms import Select2Widget, Select2MultipleWidget

from core.models import User, Examination, Department, Scheduler, UserExamination, Question, Answer


class UserExaminationReportForm(forms.Form):
    user = forms.ModelChoiceField(label='Пользователь', required=False, queryset=User.default_objects.all(), widget=Select2Widget)
    examination = forms.ModelChoiceField(label='Тестирование', required=False, queryset=Examination.default_objects.all(), widget=Select2Widget)


class UserSearchForm(forms.Form):
    department = forms.ModelChoiceField(label='Отдел', required=False, queryset=Department.objects.all(), widget=Select2Widget)


class UserExaminationSearchForm(forms.Form):
    user = forms.ModelChoiceField(label='Пользователь', required=False, queryset=User.objects.all(), widget=Select2Widget)
    examination = forms.ModelChoiceField(label='Тестирование', required=False, queryset=Examination.objects.all(), widget=Select2Widget)


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    departments = forms.ModelMultipleChoiceField(label='Отделы', required=False, queryset=Department.objects.all(), widget=Select2MultipleWidget)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'departments',  'is_staff')

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email уже занят')
        return email



class SchedulerEditForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(label='Пользователи', required=False, queryset=User.objects.all(), widget=Select2MultipleWidget)
    departments = forms.ModelMultipleChoiceField(label='Отделы', required=False, queryset=Department.objects.all(), widget=Select2MultipleWidget)

    class Meta:
        model = Scheduler
        fields = ('users', 'departments', 'examination', 'count', 'period', 'unit', 'is_active')


class SchedulerSearchForm(forms.Form):
    users = forms.ModelMultipleChoiceField(label='Пользователи', queryset=User.objects.all(), required=False, widget=Select2MultipleWidget)
    departments = forms.ModelMultipleChoiceField(label='Отделы', queryset=Department.objects.all(), required=False, widget=Select2MultipleWidget)
    examination = forms.ModelChoiceField(label='Тестирование', required=False, queryset=Examination.objects.all(), widget=Select2Widget)


class ExaminationEditForm(forms.ModelForm):

    class Meta:
        model = Examination
        fields = ('name', 'minutes_to_pass', 'department')


class QuestionEditForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('body',)


class AnswerEditForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ('body', 'is_right')


class ExaminationSearchForm(forms.Form):
    pass


class DepartmentEditForm(forms.ModelForm):
    responsible = forms.ModelMultipleChoiceField(label='Ответственные', required=False, queryset=User.objects.all(), widget=Select2MultipleWidget)
    employees = forms.ModelMultipleChoiceField(label='Сотрудники', required=False, queryset=User.objects.all(), widget=Select2MultipleWidget)

    class Meta:
        model = Department
        fields = ('name', 'responsible', 'employees')


class UserUpdateForm(forms.ModelForm):
    departments = forms.ModelMultipleChoiceField(label='Отделы', required=False, queryset=Department.objects.all(), widget=Select2MultipleWidget)

    class Meta:
        model = User
        fields = ('username', 'email', 'departments',  'is_staff')

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        id = self.initial['user_id']
        same_email_users_qs = User.objects.filter(email=email)
        if id:
            same_email_users_qs = same_email_users_qs.exclude(id=id)
        if email and same_email_users_qs:
            raise forms.ValidationError('Email уже занят')
        return email


class UserExaminationEditForm(forms.ModelForm):
    user = forms.ModelChoiceField(label='Пользователь', required=False, queryset=User.objects.all(), widget=Select2Widget)
    examination = forms.ModelChoiceField(label='Тестирование', required=False, queryset=Examination.objects.all(), widget=Select2Widget)

    class Meta:
        model = UserExamination
        fields = ('examination', 'user', 'available_from', 'complete_until')
        widgets = {
            'available_from': forms.DateTimeInput(attrs={'class': 'datetimepicker'}),
            'complete_until': forms.DateTimeInput(attrs={'class': 'datetimepicker'})
        }


class ApiUserImportForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all())

    class Meta:
        model = User
        fields = ('username', 'email')


class ApiDepartmentImportForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ('name',)
