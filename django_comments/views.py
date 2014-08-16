# coding: utf-8

from django.http import HttpResponse
from django.core.exceptions import ImproperlyConfigured
from django.views.generic.edit import FormView
from django_comments.signals import (form_invalid, form_valid, before_save,
                                     after_save)


class CreateCommentView(FormView):
    """
    Base comment view that handles comments creation
    """

    def get_content_object(self):
        """
        Gets the comment target content object
        """
        return None

    def get_plugin(self):
        """
        Returns comments plugin instance
        """

    def get_form_class(self):
        """
        Returns form class
        """
        return self.get_plugin().get_form_class(self.request)

    def form_invalid(self, form):
        """
        Case when comment form is not validate
        """
        content_object = self.get_content_object()
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
        content_object = self.get_content_object()
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
