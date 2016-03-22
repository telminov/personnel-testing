# -*- coding: utf-8 -*-

import time

from core.models import UserExamination
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-i', '--infinite',
            action='store_true',
            dest='infinite',
            default=False,
            help='Run infinite loop'
        )

    def handle(self, *args, **options):
        if options['infinite']:
            while True:
                UserExamination.fixed_started()
                time.sleep(60)
        else:
            UserExamination.fixed_started()
