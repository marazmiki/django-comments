# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext as _
from comments.models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('date_created', 'date_changed', 'is_approved', 'parent', 'remote_addr', 'forwarded_for', 'is_approved', )
