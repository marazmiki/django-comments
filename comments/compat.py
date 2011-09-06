# -*- coding: utf-8 -*-

try:
    # Uses Django 1.3 class based views
    from django.views.generic import View
    from django.utils.decorators import classonlymethod
    from django.shortcuts import render

except ImportError:
    # On earlier Django version implements View class manually
    from django.http import HttpResponseNotAllowed, HttpResponse
    from django.template import RequestContext, loader
    from functools import update_wrapper

    class classonlymethod(classmethod):
        """
        """
        def __get__(self, instance, owner):
            if instance is not None:
                raise AttributeError("This method is available only on the view class.")
            return super(classonlymethod, self).__get__(instance, owner)

    class View(object):
        """
        Intentionally simple parent class for all views. Only implements
        dispatch-by-method and simple sanity checking.
        """
        http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']
    
        def __init__(self, **kwargs):
            """
            Constructor. Called in the URLconf; can contain helpful extra
            keyword arguments, and other things.
            """
            # Go through keyword arguments, and either save their values to our
            # instance, or raise an error.
            for key, value in kwargs.iteritems():
                setattr(self, key, value)
    
        @classonlymethod
        def as_view(self, **initkwargs):
            """
            Main entry point for a request-response process.
            """
            # sanitize keyword arguments
            for key in initkwargs:
                if key in self.http_method_names:
                    raise TypeError(u"You tried to pass in the %s method name as a "
                                    u"keyword argument to %s(). Don't do that."
                                    % (key, self.__name__))
                if not hasattr(self, key):
                    raise TypeError(u"%s() received an invalid keyword %r" % (
                        self.__name__, key))
    
            def view(request, *args, **kwargs):
                cls = self(**initkwargs)
                return cls.dispatch(request, *args, **kwargs)
    
            # take name and docstring from class
            update_wrapper(view, self, updated=())
    
            # and possible attributes set by decorators
            # like csrf_exempt from dispatch
            update_wrapper(view, self.dispatch, assigned=())
            return view
    
        def dispatch(self, request, *args, **kwargs):
            # Try to dispatch to the right method; if a method doesn't exist,
            # defer to the error handler. Also defer to the error handler if the
            # request method isn't on the approved list.

            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            self.request = request
            self.args = args
            self.kwargs = kwargs
            return handler(request, *args, **kwargs)
    
        def http_method_not_allowed(self, request, *args, **kwargs):
            allowed_methods = [m for m in self.http_method_names if hasattr(self, m)]
            return HttpResponseNotAllowed(allowed_methods)
    
    def render(request, *args, **kwargs):
        """
        Returns a HttpResponse whose content is filled with the result of calling
        django.template.loader.render_to_string() with the passed arguments.
        Uses a RequestContext by default.
        """
        httpresponse_kwargs = {
            'content_type': kwargs.pop('content_type', None),
            'status': kwargs.pop('status', None),
        }
    
        if 'context_instance' in kwargs:
            context_instance = kwargs.pop('context_instance')
            if kwargs.get('current_app', None):
                raise ValueError('If you provide a context_instance you must '
                                 'set its current_app before calling render()')
        else:
            current_app = kwargs.pop('current_app', None)
            context_instance = RequestContext(request, current_app=current_app)
    
        kwargs['context_instance'] = context_instance
    
        return HttpResponse(loader.render_to_string(*args, **kwargs),
                            **httpresponse_kwargs)