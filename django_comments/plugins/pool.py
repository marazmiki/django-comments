# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.core.exceptions import ImproperlyConfigured
from django_comments.compat import import_by_path
from django_comments.exceptions import AlreadyRegistered, NoSuchPlugin
from django_comments.plugins.base import BasePlugin


class PluginPool(object):
    plugins = {}

    def get_all_plugins(self):
        return self.plugins

    def get_plugin(self, plugin):
        try:
            return self.get_all_plugins()[plugin]
        except KeyError:
            raise NoSuchPlugin('Plugin %s not registered' % plugin)

    def register(self, plugin):
        if isinstance(plugin, basestring):
            try:
                plugin = import_by_path(plugin)
            except ImportError:
                raise ImproperlyConfigured(
                    "The COMMENTS_PLUGINS setting refers to "
                    "a non-existing package: %s" % plugin
                )
        if not issubclass(plugin, BasePlugin):
            raise ValueError('Plugin must be a BasePlugin subclass')
        if plugin.codename in self.plugins:
            raise AlreadyRegistered('Plugin %s is already registered' % plugin)

        self.plugins[plugin.codename] = plugin


plugin_pool = PluginPool()