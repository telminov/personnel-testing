# -*- coding: utf-8 -*-

import time

from core.models import UserExamination
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--deamon',
            action='store_true',
            dest='deamon',
            default=False,
            help='Run as deamon'
        )

    def handle(self, *args, **options):
        if options['deamon']:
            while True:
                UserExamination.fixed_expired()
                time.sleep(60 * 30)  # 30 min
        else:
            UserExamination.fixed_expired()
