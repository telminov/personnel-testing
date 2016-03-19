# -*- coding: utf-8 -*-
import json

import six
from django.db import models


class JSONField(models.TextField):
    def __init__(self, *args, **kwargs):
        default = kwargs.get('default', '{}')
        if isinstance(default, (list, dict)):
            kwargs['default'] = json.dumps(default)
        models.TextField.__init__(self, *args, **kwargs)

    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""
        if value is None or value == '':
            return {}
        return json.loads(value)

    def get_db_prep_save(self, value, connection, **kwargs):
        """Convert our JSON object to a string before we save"""
        if value is None and self.null:
            return None
        # default values come in as strings; only non-strings should be
        # run through `dumps`
        if not isinstance(value, six.string_types):
            value = json.dumps(value)
        return value

    def deconstruct(self):
        name, path, args, kwargs = super(JSONField, self).deconstruct()
        if self.default == '{}':
            del kwargs['default']
        return name, path, args, kwargs
