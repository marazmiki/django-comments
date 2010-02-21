# -*- coding: utf-8 -*-

from django.contrib import admin
from django.conf import settings
from django.core import urlresolvers
from django.utils.translation import ugettext as _
from comments.models import Comment

class CommentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, dict(fields=['content', 'parent_comment', 'is_approved'])),
        (_('IP address'),     dict(fields=['remote_addr', 'forwarded_for',])),
        (_('Date and time'),  dict(fields=['date_created', 'date_changed'])),
        (_('Content object'), dict(fields=['content_type', 'object_pk'])),
    ]

admin.site.register(Comment, CommentAdmin)

