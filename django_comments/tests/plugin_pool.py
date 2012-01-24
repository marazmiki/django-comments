# -*- coding: utf-8 -*-

from django import test
from django.core.exceptions import ImproperlyConfigured
from django_comments.plugins import plugin_pool
from django_comments.exceptions import NoSuchPlugin, AlreadyRegistered
from django_comments.defaults import DjangoCommentPlugin

class RegisterPluginsTest(test.TestCase):
    """
    Test cases for registering plugin class in pool
    """
    def test_raise_improperly_configured_exception_if_no_module(self):
        """
        Tests that ImproperlyConfigured exception is raised when 
        module given in 'register' argument couldn't be found
        """
        def raises():
            """
            Raises exception
            """
            plugin_pool.register('foo.bar.baz')
        self.assertRaises(ImproperlyConfigured, raises)

    def test_raise_improperly_configured_exception_if_class_not_found(self):
        """
        Tests that ImproperlyConfigured exception is raised when 
        module given in 'register' argument exists, but plugin 
        class couldn't be found
        """
        def raises():
            """
            Raises exception
            """
            plugin_pool.register('comments.defaults.DjangoCommentPlugin_')

        self.assertRaises(ImproperlyConfigured, raises)

    def test_raise_already_registered(self):
        """
        Tests that AlreadyRegistered exception is raised when same plugins
        tried to be registered twice. 
        """
        def raises():
            """
            Raises exception
            """
            plugin_pool.register('comments.defaults.DjangoCommentPlugin')
            plugin_pool.register('comments.defaults.DjangoCommentPlugin')
        self.assertRaises(AlreadyRegistered, raises)

    def test_raise_value_error_if_wrong_plugin_class(self):
        """
        Tests that ValueError exception is raised when given class not a
        Plugin instance
        """
        def raises():
            """
            Raises exception
            """
            plugin_pool.register('django.contrib.comments.models.Comment')
        self.assertRaises(ValueError, raises)


class GetPluginFromPoolTest(test.TestCase):
    def test_get_plugin(self):
        assert plugin_pool.get_plugin('django').__class__ is DjangoCommentPlugin

    def test_raise_exception_if_get_non_existant_plugin(self):
        def raises():
            """
            Raises exception
            """
            plugin_pool.get_plugin('non_existant_plugin')
        self.assertRaises(NoSuchPlugin, raises)