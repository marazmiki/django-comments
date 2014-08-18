# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.core.signals import Signal


args_base = ['request', 'form', 'content_object']
args_full = args_base + ['comment']


form_invalid = Signal(providing_args=args_base)
form_valid = Signal(providing_args=args_base)
pre_save = Signal(providing_args=args_full)
post_save = Signal(providing_args=args_full)
