from django import forms
from core.models import UserExaminationAnswer, UserExamination


class UserExaminationAnswerForm(forms.ModelForm):

    class Meta:
        model = UserExaminationAnswer
        fields = []

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('ueq')
        user_examination = kwargs.pop('user_examination')
        self.fields['ueq'].queryset = UserExamination.objects.

        super(UserExaminationAnswerForm, self).__init__(*args, **kwargs)
