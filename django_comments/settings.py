# coding: utf-8

from django.conf import settings

get = lambda attr, default: getattr(settings, attr, default)

DEFAULT_PLUGIN = get('COMMENTS_DEFAULT_PLUGIN', 'django_comments.defaults.DjangoCommentPlugin')
PLUGINS = get('COMMENTS_PLUGINS', (DEFAULT_PLUGIN, ))

