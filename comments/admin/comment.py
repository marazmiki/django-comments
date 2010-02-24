# -*- coding: utf-8 -*-

from django.contrib import admin
from django.conf import settings
from django.core import urlresolvers
from django.utils.translation import ugettext as _
from comments.models import Comment

class CommentAdmin(admin.ModelAdmin):
    raw_id_fields = ['parent_comment', ]
    fieldsets = [
        (None, dict(fields=['content', 'parent_comment', 'is_approved'])),
        (_('IP address'),     dict(fields=['remote_addr', 'forwarded_for',], classes=['collapse'])),
        (_('Date and time'),  dict(fields=['date_created', 'date_changed'],  classes=['collapse'])),
        (_('Content object'), dict(fields=['content_type', 'object_pk'],     classes=['collapse'])),
    ]

admin.site.register(Comment, CommentAdmin)

