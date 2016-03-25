from django import forms

from django_select2.forms import Select2Widget, Select2MultipleWidget

from core.models import User, Examination, Department


class UserExaminationReportForm(forms.Form):
    user = forms.ModelChoiceField(label='Пользователь', required=False, queryset=User.objects.all(), widget=Select2Widget)
    examination = forms.ModelChoiceField(label='Тестирование', required=False, queryset=Examination.objects.all(), widget=Select2Widget)


class UserManagementSearchForm(forms.Form):
    department = forms.ModelChoiceField(label='Отдел', required=False, queryset=Department.objects.all(), widget=Select2Widget)


class UserManagementCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    departments = forms.ModelMultipleChoiceField(label='Отделы', required=False, queryset=Department.objects.all(), widget=Select2MultipleWidget)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'departments',  'is_staff')


class UserManagementUpdateForm(forms.ModelForm):
    departments = forms.ModelMultipleChoiceField(label='Отделы', required=False, queryset=Department.objects.all(), widget=Select2MultipleWidget)

    class Meta:
        model = User
        fields = ('username', 'email', 'departments',  'is_staff')


class ApiUserImportForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class ApiDepartmentImportForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ('name',)
