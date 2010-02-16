# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('comments.views',
    url(
        regex = '^add/$',
        view  = 'create',
        name  = 'comments_create',
    ),
    url(
        regex = '^reply/(?P<parent_id>\d+)/$',
        view  = 'create',
        name  = 'comments_reply',
    ),
)

