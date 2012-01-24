# -*- coding: utf-8 -*-

from django import test
from django.conf import settings
from django.contrib import comments as django_comments
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest
from django_comments.plugins import plugin_pool
from django_comments.exceptions import AlreadyRegistered, NoSuchPlugin

class EnvironmentTest(test.TestCase):
    """
    Environment test cases
    """
    def test_request_context_processors_installed(self):
        """
        Tests that `request` context processor is installed
        """
        assert 'django.core.context_processors.request' in \
        settings.TEMPLATE_CONTEXT_PROCESSORS


class DjangoDefaultCommentsTest(test.TestCase):
    """
    """
    def setUp(self):
        self.plugin = plugin_pool.get_plugin('django')
        self.request = HttpRequest()

    def test_default_model(self):
        assert self.plugin.get_model(self.request) is django_comments.models.Comment

    def test_default_form(self):
        assert self.plugin.get_form(self.request) is django_comments.forms.CommentForm

    def test_default_urlpatterns(self):
        assert self.plugin.get_urlpatterns() is django_comments.urls.urlpatterns


from django_comments.tests.plugin_pool import *