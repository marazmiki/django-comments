# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext as _
from .models import GuestComment

class GuestCommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'content_object', 'date_created', 'author')
    fieldsets = (
        (None, {'fields':['author', 'email', 'website', 'content']}),
        (_('Parent comment'), {'fields': ['parent_comment']}),
        (_('Generic relation'), {'fields': ['content_type', 'object_id']}),        
    )

admin.site.register(GuestComment, GuestCommentAdmin)