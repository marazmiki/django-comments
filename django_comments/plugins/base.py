# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.core.exceptions import ImproperlyConfigured
from django.forms.models import modelform_factory
from django_comments.views import CreateCommentView


class AbstractBasePlugin(object):
    def __init__(self, *args, **kwargs):
        pass

    def get_model(self):
        raise NotImplementedError()

    def get_queryset(self):
        raise NotImplementedError()

    def get_form_class(self):
        pass

    def get_urlpatterns(self):
        return [] + self.get_urls()

    def get_urls(self):
        return []

    def get_view_class(self):
        return None

    def prepare_object(self, request, form, content_object):
        return None

    def save_comment(self, form):
        pass

    def before_save(self, form):
        pass

    def is_need_save(self):
        pass


class PluginBase(AbstractBasePlugin):
    pass


class ThreadPlugin(PluginBase):
    def get_form_class(self):
        is_reply = isinstance(self.content_object, self.model)

        if self.request.user.is_authenticated():
            if is_reply:
                return CommentReplyAuthenticatedForm
            else:
                return CommentReplyAnonymousForm
        else:
            if is_reply:
                return CommentCreateAuthenticatedForm
            else:
                return CommentCreateAnonymousForm