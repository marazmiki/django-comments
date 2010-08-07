# -*- coding: utf-8 -*-

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

class CommentViewTest(TestCase):
    view_name = 'comments_new'

    def setUp(self):
        self.client = client.Client()
        self.url    = reverse(self.view_name)

    def get(self, data=dict(), meta=dict(), url=None):
        return self.client.get(url or self.url, data, **meta)

    def post(self, data=dict(), meta=dict(), url=None):
        return self.client.post(url or self.url, data, **meta)

    def ajax_get(self, data=dict(), meta=dict(), url=None):
        meta.update(HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        return self.get(data, meta, url)

    def ajax_post(self, data=dict(), meta=dict(), url=None):
        meta.update(HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        return self.post(data, meta, url)


# --------------------------------------------------------------------------- #

from .environment import *
from .views import *
from comments_plugins.guest.tests import *
#from comments_plugins.authorized.tests import *