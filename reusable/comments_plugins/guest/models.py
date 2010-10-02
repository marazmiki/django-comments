# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.db import models
from reusable.comments.models import AbstractComment
from reusable.comments.plugins import register

# --------------------------------------------------------------------------- #

class GuestComment(AbstractComment):
    author = models.CharField(max_length=255,
        verbose_name = _('Your name'),
        help_text    = _('This field is required')
    )
    email = models.EmailField(
        verbose_name = _('Your E-mail'),
        help_text    = _('Will not be shown nobody')                               
    )
    website = models.URLField(
        verbose_name = _('Your website'),
        help_text    = _('An address of your website or blog. Optional'),
        blank=True,
        null=True,
        verify_exists=False
    )

    class Meta:
        app_label = 'comments'
        ordering = ('tree_id', 'lft', 'date_created', )

# --------------------------------------------------------------------------- #

register(GuestComment)