# -*- coding: utf-8 -*-

from django.test import TestCase, client
from comments.tests import create_user, get_content_object, USERNAME, PASSWORD
from comments.models import Comment, LastReadedComment

class LastReadedTest(TestCase):
    urls = 'comments.tests.urls'

    def setUp(self):
        self.user_john = create_user(USERNAME)
        self.user_jane = create_user('Jane')
        self.object = get_content_object()
        self.client = client.Client()

    def auth(self):
        self.client.login(username=USERNAME,password=PASSWORD)

