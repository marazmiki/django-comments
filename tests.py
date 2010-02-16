# -*- coding: utf-8 -*-

from django.test import TestCase, client
from django.core import urlresolvers, exceptions
from django.contrib.contenttypes.models import ContentType
from comments.forms import CommentForm

# --------------------------------------------------------------------------- #

class BaseCommentTest(TestCase):
    def setUp(self):
        self.client = client.Client()
        self.url    = self.reverse_view()

    def reverse_view(self):
        view = self.get_view_name()

        if view:
            return urlresolvers.reverse(view)

    def get_view_name(self):
        return None

# --------------------------------------------------------------------------- #

class CreateCommentTest(BaseCommentTest):
    def get_valid_post_data(self):
        object = ContentType.objects.get(pk=1)
        return dict(
            author  = 'John Doe',
            email   = 'john@doe.com',
            content = 'Hello world',
            object_id       = object.pk,
            content_type_id = ContentType.objects.get_for_model(object),
        )

    def get_view_name(self):
        return 'comments_create'

    def testCreateViewExists(self):
        resp = self.client.get(self.url)
        self.assertEquals(200, resp.status_code)

    def testTemplateName(self):
        resp = self.client.get(self.url)
        self.assertEquals('comments/create.html', resp.template.name)

    def testFormInTemplateContext(self):
        resp = self.client.get(self.url)
        self.assertTrue(isinstance(resp.context.get('form'), CommentForm))

    def testPostNewComment(self):
        post = ContentType.objects.get(pk=1)
        resp = self.client.post(self.url, self.get_valid_post_data())
        self.assertEquals(200, resp.status_code)

# --------------------------------------------------------------------------- #

class ReplyCommentTest(BaseCommentTest):
    def get_view_name(self):
        return 'comments_reply'

        


