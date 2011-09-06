from django.db import models
from django.conf import settings as settings
from comments.plugins import plugin_pool
from comments.settings import PLUGINS

for plugin in PLUGINS:
    plugin_pool.register(plugin)

