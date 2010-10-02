# -*- coding: utf-8 -*-

from reusable.comments.forms import forms, CommentForm
from .models import GuestComment

# --------------------------------------------------------------------------- #

class GuestCommentForm(CommentForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model  = GuestComment
        fields = (
            'author', 'email', 'website', 'content',
            'content_type', 'object_id',
        )

    class CommentsMeta:
        fields = ['author', 'email', 'website', 'content']