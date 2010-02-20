# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        object = kwargs.pop('object', None)

        if object:
            if not kwargs.get('initial'):
                kwargs['initial'] = dict()

            kwargs['initial'].update(
                object_pk    = object.pk,
                content_type = ContentType.objects.get_for_model(object).pk
            )

        super(CommentForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Comment
        exclude = ('date_created', 'date_changed', 'is_approved', 'parent', 'remote_addr', 'forwarded_for', 'is_approved', )

class ReplyForm(CommentForm):
    def __init__(self, *args, **kwargs):
        super(ReplyForm, self).__init__(*args, **kwargs)
        del self.fields['content_type']
        del self.fields['object_pk']