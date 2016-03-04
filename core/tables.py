import django_tables2 as tables

from core.models import UserExamination


class UserExaminationTable(tables.Table):
    class Meta:
        model = UserExamination
        exclude = ('id',)