# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django_comments.plugins import plugin_pool
from django_comments.settings import PLUGINS, SYSTEM_DEFAULT_PLUGIN


def default_plugin_enabled():
    return SYSTEM_DEFAULT_PLUGIN in PLUGINS


for plugin in PLUGINS:
    plugin_pool.register(plugin)