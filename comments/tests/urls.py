# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from comments.urls import urlpatterns as comments_urlpatterns
urlpatterns = patterns('comments.tests',
    url(
        regex = '^templatetags/insert_comments/$',
        view  = 'templatetags.view_insert_comments',
        name  = 'templatetags_insert_comment',
    ),
    url(
        regex = '^templatetags/get_comments_count/$',
        view  = 'templatetags.view_get_comments_count',
        name  = 'templatetags_get_comments_count',
    ),
) + comments_urlpatterns

