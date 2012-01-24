# -*- coding: utf-8 -*-

from django.conf import settings

DEFAULT_PLUGIN = getattr(settings, 'COMMENTS_DEFAULT_PLUGIN', 
    'django_comments.defaults.DjangoCommentPlugin')
PLUGINS = getattr(settings, 'COMMENTS_PLUGINS', (DEFAULT_PLUGIN, ))

