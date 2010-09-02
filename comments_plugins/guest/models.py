# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.db import models
from comments.models import AbstractComment
from comments.plugins import register

# --------------------------------------------------------------------------- #

class GuestComment(AbstractComment):
    author  = models.CharField(max_length=255)
    email   = models.EmailField()
    website = models.URLField(blank=True, null=True, verify_exists=False)

    class Meta:
        app_label = 'comments'
        ordering = ('tree_id', 'lft', 'date_created', )

# --------------------------------------------------------------------------- #

register(GuestComment)