# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from comments.models import AbstractComment as Comment

# --------------------------------------------------------------------------- #

class CommentForm(forms.ModelForm):
    redirect_to = forms.CharField(required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        object = kwargs.pop('object', None)

        if object:
            kwargs['initial'] = kwargs.get('initial') or dict()
            kwargs['initial'].update(
                object_id    = object.pk,
                content_type = ContentType.objects.get_for_model(object).pk
            )

        super(CommentForm, self).__init__(*args, **kwargs)

        #print self.fields
        #self.fields['object_id'].widget    = forms.HiddenInput()
        #self.fields['content_type'].widget = forms.HiddenInput()

    class Meta:
        model = Comment
        fields = ('content', 'object_id', 'content_type', )