# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from comments.urls import urlpatterns as comments_urlpatterns

urlpatterns = patterns('comments.tests.views',
    url(
        regex = '^templatetags/insert_comments_brief/$',
        view  = 'insert_comments_brief',
        name  = 'test_view_insert_comment_brief',
    ),
    url(
        regex = '^templatetags/insert_comments_full/$',
        view  = 'insert_comments_full',
        name  = 'test_view_insert_comment_full',
    ),
) + comments_urlpatterns
