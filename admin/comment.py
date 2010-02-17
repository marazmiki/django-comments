# -*- coding: utf-8 -*-

from django.contrib import admin
from django.conf import settings
from django.core import urlresolvers
from django.utils.translation import ugettext as _
from comments.models import Comment

class CommentAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Comment, CommentAdmin)

