# -*- coding: utf-8 -*-

from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
from django_comments.exceptions import AlreadyRegistered, NoSuchPlugin
from django_comments.views import CreateView

class BasePlugin(object):
    """
    Base plugin class
    """
    # Plugin codename used in template tags or URL patterns
    codename = ''

    def __init__(self, *args, **kwargs):
        """
        The class constructor
        """
        if not getattr(self, 'codename'):
            raise ImproperlyConfigured, 'Comment plugin must have the `codename` attribute' 

    def get_model(self, request):
        """
        Returns the comment model class
        """
        raise NotImplementedError, 'Method get_model() must return comment model class'

    def get_queryset(self, request, object):
        """
        Returns the comments queryset. Usable for comments list
        """
        raise NotImplementedError, 'Method get_queryset() must return comments QuerySet class'
        
    def get_form(self, request, kwargs={}):
        """
        Returns the comment model form class
        """
        raise NotImplementedError, 'Method get_form() must return comment form class'

    def get_urlpatterns(self):
        """
        Returns set of urlconf in standart 'urlpatterns' format        
        """
        raise NotImplementedError, 'Method get_urlpatterns() must return URLConfs'

    def get_view(self):
        """
        Returns comment view object
        """
        return CreateView

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
        raise NoSuchPlugin, 'Plugin %s not registered' % plugin 


    def register(self, plugin):
        """
        Register new comment plugin in pool
        """
        # Try to import the package

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
                    "The COMMENTS_PLUGINS setting refers to "\
                    "a non-existing package: %s" % plugin
                )

        if not issubclass(plugin, BasePlugin):
            raise ValueError, 'Plugin must be a BasePlugin subclass'

        if plugin.codename in self.plugins:
            raise AlreadyRegistered, 'Plugin %s is already registered' % plugin

        self.plugins[plugin.codename] = plugin()

plugin_pool = PluginPool()
