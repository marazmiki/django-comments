# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from reusable.comments.models import AbstractComment as Comment

# --------------------------------------------------------------------------- #

class CommentForm(forms.ModelForm):
    redirect_to = forms.CharField(required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['object_id'].widget    = forms.HiddenInput()
        self.fields['content_type'].widget = forms.HiddenInput()

    class Meta:
        model = Comment
        fields = ('content', 'object_id', 'content_type', )