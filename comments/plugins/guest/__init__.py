# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.utils.translation import ugettext_lazy as _
from django.utils.simplejson import dumps
from django.template import RequestContext, loader
from django.contrib import messages
from comments.plugins import CommentPlugin
from .forms import GuestCommentForm
from .models import GuestComment

# --------------------------------------------------------------------------- #

class GuestCommentPlugin(CommentPlugin):
    def get_form(self):
        return GuestCommentForm

    def get_model(self):
        return GuestComment

    def json_response(self, data):
        return HttpResponse(dumps(data), mimetype='application/x-json')

    def on_success(self, request, form, comment):
        """
        Обработчик, вызываемый при успешном создании комментария

        Принимает следующие параметры:
          * request
          * form
          * comment

        Возвращает:
          * Объект HttpResponse
        """
        message = _('Comment successfully created')

        if request.is_ajax():
            return self.json_response(
                dict(
                    success = True,
                    message = unicode(message),
                    comment = loader.render_to_string('comments_plugins/guest/item.html',
                        dict(
                            comment = comment,
                        ),
                        context_instance=RequestContext(request)
                    )
                )
            )
                
        messages.success(request, message)

        return redirect(
            request.POST.get('redirect_to') or \
            request.META.get('HTTP_REFERER', '/')
        )

    def on_failure(self, request, form):
        """
        Обработчик, вызываемый при ошибке создания комментария
        """
        message = _('An error occured')
        errors = dict()
        
        for e in form.errors:
            errors[e] = unicode(form.errors[e])

        if request.is_ajax():
            return self.json_response(
                dict(
                    success = False,
                    message = unicode(message),
                    errors = errors,
                )
            )

        messages.error(request, message)

        return render_to_response('comments_plugins/guest/errors.html',
            dict(
                form = form,
            ),
            context_instance=RequestContext(request),
        )
        
        
