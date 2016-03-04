from django import forms

from django_select2.forms import Select2Widget

from core.models import User, Examination


class UserExaminationReportForm(forms.Form):
    user = forms.ModelChoiceField(label='Пользователь', required=False, queryset=User.objects.all(), widget=Select2Widget)
    examination = forms.ModelChoiceField(label='Тестирование', required=False, queryset=Examination.objects.all(), widget=Select2Widget)
