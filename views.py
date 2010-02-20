# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson
from django.http import HttpResponse
from comments.forms import CommentForm

def create(request, parent_id=None):
    """
    Post a new comment
    """
    parent = get_object_or_404(Comment, pk=parent_id) if parent_id else None

    def get_object():
        """
        Returns instance of object which will be commented
        """
        object_id    = request.POST.get('object_id')
        content_type = request.POST.get('content_type')

        from django.contrib.contenttypes.models import ContentType
        return ContentType.objects.get(pk=1)

    result = dict()

    if request.method == 'POST':
        form   = CommentForm(request.POST)
        valid  = form.is_valid()
        object = get_object()

        if valid:
            comment = form.save(commit=False)
            comment.parent_comment = parent
            comment.content_object = object
            comment.remote_addr    = request.META.get('REMOTE_ADDR')
            comment.forwarded_for  = request.META.get('HTTP_X_FORWARDRED_FOR')
            comment.save()

            if request.is_ajax():
                result.update(
                    comment = render_to_string('comments/item.html',{'comment': comment, }),
                    parent  = parent,
                    comment_id = comment.pk,
                )

                return HttpResponse(simplejson.dumps(result))

            else:
                return redirect('/') # TODO: correct redirect URL

        result.update(success=valid)

    else:
        form = CommentForm()

    result.update(form=form)

    return render_to_response('comments/create.html', result,
        context_instance=RequestContext(request)
    )