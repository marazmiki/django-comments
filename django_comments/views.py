# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import View
from django_comments.signals import form_invalid as form_invalid_signal,\
    form_valid as form_valid_signal, before_save as before_save_signal,\
    after_save as after_save_signal


class CreateView(View):
    """
    Base comment view that handles comments creation
    """
    http_method_names = ['get', 'post']
    plugin = None

    def __init__(self, *args, **kwargs):
        """
        The comment view class constructor
        """
        super(CreateView, self).__init__(*args, **kwargs)
        if not getattr(self, 'plugin'):
            raise ImproperlyConfigured, 'Plugin for comment not given'

    def get_content_object(self, request, kwargs):
        """
        Gets the comment target content object
        """
        return None

    def get(self, request, **kwargs):
        """
        Handles GET request
        """
        raise NotImplemented, 'Code that handles GET request not implemented'

    def post(self, request, **kwargs):
        """
        Handles POST request
        """
        object = self.get_content_object(request, self.kwargs)
        form = self.plugin.get_form(request, self.kwargs)(
            request.POST or None,
            request.FILES or None)
        if form.is_valid():
            form_valid_signal.send(request=request, form=form, content_object=object, sender=None)
            comment = form.save(commit=False)

            if getattr(self.plugin, 'content_object_field') and object:
                setattr(comment, self.plugin.content_object_field, object)

            # Before save hook
            before_save_signal.send(request=request, form=form, content_object=object, comment=comment, sender=None)
            before_save = self.before_save(request, form, comment,
                self.kwargs)
            if type(before_save) is HttpResponse:
                return before_save

            # Save the comment
            comment.save()

            # After save hook
            after_save_signal.send(request=request, form=form, content_object=object, comment=comment, sender=None)
            response = self.after_save(request, form, comment, self.kwargs)

            if isinstance(response, HttpResponse):
                return response

            raise ImproperlyConfigured, 'after_save method must '\
                                        'return a HttpResponse instance'
        # Form validation error happens
        else:
            form_invalid_signal(request=request, form=form, content_object=object, sender=sender)
            return self.failure(request, form, object, self.kwargs)

    def before_save(self, request, form, comment, kwargs={}):
        """
        Handles case before comment save if form filled correctly.  
        """
        return None

    def after_save(self, request, form, comment, kwargs={}):
        """
        Handles case after comment save if form filled correctly.  
        """
        return None

    def failure(self, request, form, object, kwargs={}):
        """
        Handles case if form is incorrect.  
        """
        raise NotImplemented, 'Validation error handling not implemented'