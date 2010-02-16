# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from comments.forms import CommentForm

def create(request, parent_id=None):
    """
    Post a new comment
    """

    def get_parent():
        """
        Returns a parent comment if reply created
        """
        if parent_id:
            parent = get_object_or_404(Comment, pk=parent_id)
        else:
            parent = None

    def get_object():
        """
        Returns instance of object which will be commented
        """
        return None

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.parent = get_parent()
            comment.object = get_object()
            comment.save()
    else:
        form = CommentForm()

    return render_to_response('comments/create.html',
        dict(
            form=form,
        ),
        context_instance=RequestContext(request)
    )