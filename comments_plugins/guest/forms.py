# -*- coding: utf-8 -*-

from comments.forms import forms, CommentForm
from .models import GuestComment

# --------------------------------------------------------------------------- #

class GuestCommentForm(forms.ModelForm):
    class Meta:
        model  = GuestComment
        fields = (
            'author', 'email', 'website', 'content',
            'content_type', 'object_id',
        )