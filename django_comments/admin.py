# coding: utf-8

from django.contrib import admin
from django_comments.models import Comment, default_plugin_enabled


class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'author_name', 'date_created']
    date_hierarchy = 'date_created'


if default_plugin_enabled():
    admin.site.register(Comment, CommentAdmin)