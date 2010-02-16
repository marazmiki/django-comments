# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext as _

class CommentForm(forms.Form):
    def save(self, *args, **kwargs):
        class Mock(object):
            def __init__(self, *args, **kwargs):
                pass
            def save(self, *args, **kwargs):
                pass
        return Mock()
