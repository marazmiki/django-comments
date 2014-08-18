# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.http import HttpResponse
from django.core.exceptions import ImproperlyConfigured
from django.views.generic.edit import FormView
from django_comments.plugins import plugin_pool
from django_comments.signals import (form_invalid, form_valid,
                                     pre_save, post_save)


class CommentMixin(object):
    def dispatch(self, *args, **kwargs):
        entry = super(CommentMixin, self).dispatch(*args, **kwargs)
        self.content_object = self.get_content_object()
        return entry

    def get_content_object(self):
        return None

    def get_plugin(self):
        return plugin_pool.get_plugin()(request=self.request,
                                        content_object=self.get_content_object())

    def get_form_class(self):
        return self.get_plugin().get_form_class()


class CreateCommentView(CommentMixin, FormView):
    def form_invalid(self, form):
        content_object = self.content_object
        form_invalid.send(sender=None,
                          form=form,
                          content_object=content_object,
                          request=self.request)
        return self.get_plugin().failure(form=form,
                                         request=self.request,
                                         content_object=content_object)

    def form_valid(self, form):
        """
        Form
        """
        content_object = self.content_object
        plugin = self.get_plugin()

        form_valid.send(sender=None,
                        form=form,
                        content_object=content_object,
                        request=self.request)

        comment = plugin.prepare_object(request=self.request,
                                        form=form, content_object=content_object)

        before_save.send(sender=None, form=form, content_object=content_object,
                         request=self.request)

        bh = plugin.before_save(form, comment)

        if isinstance(bh, HttpResponse):
            return bh

        comment.save()

        after_save.send(sender=None, form=form, content_object=content_object,
                        comment=comment, request=self.request)

        response = self.after_save(form, comment, self.kwargs)

        if isinstance(response, HttpResponse):
            return response
        raise ImproperlyConfigured('after_save method must return a '
                                   'HttpResponse instance')
