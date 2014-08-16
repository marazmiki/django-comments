# coding: utf-8

from django.core.exceptions import ImproperlyConfigured
from django.forms.models import modelform_factory
from django_comments.views import CreateCommentView


class BasePlugin(object):
    """
    Base plugin class
    """
    codename = ''
    model = None
    queryset = None
    form_class = None
    template_name = None

    def __init__(self, *args, **kwargs):
        """
        The class constructor
        """
        if not self.codename:
            raise ImproperlyConfigured('Comment plugin must have '
                                       'the `codename` attribute')

    def get_model(self, request):
        """
        Returns the comment model class
        """
        if self.model:
            return self.model
        raise NotImplementedError('Please define `model` attribute '
                                  'or override get_model() method')

    def get_queryset(self, request, content_object):
        """
        Returns the comments queryset. Usable for comments list
        """
        if self.queryset:
            return self.queryset
        return self.get_model(request)._defaul_manager.all()

    def get_comments_count(self, request, content_object):
        """
        Returns number of comments for given `content_object`
        """
        return self.get_queryset(request, content_object).count()

    def get_form_class(self, request):
        """
        Returns the comment model form class
        """
        if self.form_class:
            return self.form_class
        return modelform_factory(self.get_model())

    def get_urlpatterns(self):
        """
        Returns set of urlconf in standart 'urlpatterns' format
        """
        return []

    def get_view(self):
        """
        Returns comment view object
        """
        return CreateCommentView

    def prepare_object(self, request, form, content_object):
        return None
