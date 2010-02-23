# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext as _
from comments.models import Comment, CommentSettings

class CommentSettingsAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'enabled', 'premoderate', 'level_limit']
    fieldsets = [
        (None, dict(fields=['enabled', 'premoderate', 'level_limit'])),
        (_('Content object'), dict(fields=['content_type', 'object_pk'], classes=['collapse'])),
    ]

admin.site.register(CommentSettings, CommentSettingsAdmin)
