# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.template import Library
from django.template.defaulttags import URLNode, TemplateSyntaxError, kwarg_re

register = Library()


@register.filter
def get_by_key(dictionary, key):
    return dictionary.get(key)
