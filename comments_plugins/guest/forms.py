# -*- coding: utf-8 -*-

from comments.forms import forms, CommentForm
from .models import GuestComment

# --------------------------------------------------------------------------- #

class GuestCommentForm(CommentForm):
    class Meta:
        model  = GuestComment
        fields = (
            'author', 'email', 'website', 'content',
            'content_type', 'object_id',
        )

    class CommentsMeta:
        fields = ['author', 'email', 'website', 'content']