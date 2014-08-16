# coding: utf-8

from django.conf.urls import url
from django_comments.plugins.base import BasePlugin
from django_comments.models import Comment


class DefaultCommentPlugin(BasePlugin):
    """
    Base plugin class
    """
    codename = 'default'
    template_name = 'django_comments/default/insert_comments.html'
    model = Comment

    def get_urlpatterns(self):
        return [
            url(r'^preview/$', self.preview_comment, name='comments_preview'),
        ]

    def preview_comment(self, request):
        pass