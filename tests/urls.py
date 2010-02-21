# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from comments.urls import urlpatterns as comments_urlpatterns
urlpatterns = patterns('comments.tests',
    url(
        regex = '^templatetags/insert_comments/$',
        view  = 'templatetags.view_insert_comments',
        name  = 'templatetags_insert_comment',
    ),
) + comments_urlpatterns

