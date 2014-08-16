# coding: utf-8

from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
from django_comments.exceptions import AlreadyRegistered, NoSuchPlugin
from django_comments.plugins.base import BasePlugin


class PluginPool(object):
    """
    Registered comment plugins pool class
    """
    plugins = {}

    def get_all_plugins(self):
        """
        Returns the dict of all registered plugins
        """
        return self.plugins

    def get_plugin(self, plugin):
        """
        Returns plugin class by its codename
        """
        plugins = self.get_all_plugins()

        if plugin in plugins:
            return plugins[plugin]
        raise NoSuchPlugin('Plugin %s not registered' % plugin)

    def register(self, plugin):
        """
        Register new comment plugin in pool
        """
        if isinstance(plugin, basestring):
            try:
                module, cls = plugin.rsplit('.', 1)
                module = import_module(module)
                plugin = getattr(module, cls)

            except AttributeError:
                raise ImproperlyConfigured(
                    "The %s module hasn't a %s class" % (module, cls)
                )
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
