# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.conf import settings


get = lambda attr, default: getattr(settings, attr, default)


SYSTEM_DEFAULT_PLUGIN = 'django_comments.plugins.default.DefaultCommentPlugin'

DEFAULT_PLUGIN = get('COMMENTS_DEFAULT_PLUGIN', SYSTEM_DEFAULT_PLUGIN)
PLUGINS = get('COMMENTS_PLUGINS', (DEFAULT_PLUGIN, ))

