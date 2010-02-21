# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext as _
from comments.models import Comment, CommentSettings

class CommentSettingsAdmin(admin.ModelAdmin):
    pass

admin.site.register(CommentSettings, CommentSettingsAdmin)
