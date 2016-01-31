# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
import random
import time
from StringIO import StringIO

from django.core.management.base import BaseCommand

from core.models import Scheduler


class Command(BaseCommand):
    def handle(self, *args, **options):
        Scheduler.check_user_examinations()
