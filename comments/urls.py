# -*- coding: utf-8 -*-

from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('comments.views',
    url(
        regex = '^new/$',
        view  = 'new',
        name  = 'comments_new'
    ),
    url(
        regex = '^reply/(?P<parent_id>\d+)/$',
        view  = 'reply',
        name  = 'comments_reply'
    ),
)