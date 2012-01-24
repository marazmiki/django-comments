from django.db import models
from django.conf import settings as settings
from django_comments.plugins import plugin_pool
from django_comments.settings import PLUGINS

for plugin in PLUGINS:
    plugin_pool.register(plugin)
