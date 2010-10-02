# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from reusable.comments.models import AbstractComment

# --------------------------------------------------------------------------- #

class AuthorizedUserRequired(models.Model):
    user = models.ForeignKey(User)

    class Meta:
        app_label = 'comments'
