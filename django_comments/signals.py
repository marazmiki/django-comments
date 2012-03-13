# -*- coding: utf-8 -*-

from django.core.signals import Signal

form_invalid = Signal(providing_args=['request', 'form', 'content_object'])
form_valid = Signal(providing_args=['request', 'form', 'content_object'])
before_save = Signal(providing_args=['request', 'form', 'content_object', 'comment'])
after_save = Signal(providing_args=['request', 'form', 'content_object', 'comment'])