# -*- coding: utf-8 -*-

from django.test import TestCase, client
from django.core import urlresolvers, exceptions
from django.contrib.contenttypes.models import ContentType
from django.utils import simplejson
from comments.forms import CommentForm
from comments.models import Comment

# --------------------------------------------------------------------------- #

class BaseCommentTest(TestCase):
    """
    Base test suite
    """
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
    def setUp(self):
        super(CreateCommentTest, self).setUp()
        self.object = ContentType.objects.get(pk=1)

    def get_valid_post_data(self):
        return dict(
            content = 'Hello world',
            object_pk    = self.object.pk,
            content_type = ContentType.objects.get_for_model(self.object).pk,
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

    def testPostNewCommentSuccess(self):
        resp = self.client.post(self.url, self.get_valid_post_data())
        self.assertEquals(302, resp.status_code)

    def testAjaxPostNewCommentSuccess(self):
        resp = self.client.post(self.url, self.get_valid_post_data(), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        json = simplejson.loads(resp.content)

        self.assertEquals(200, resp.status_code)
        self.assertTrue(json.has_key('comment'))
        self.assertTrue(json.has_key('parent'))
        self.assertTrue(json.get('parent') is None)

    def testPostNewCommentFailEachField(self):
        data = self.get_valid_post_data()

        for key, value in data.items():
            del data[key]
            resp = self.client.post(self.url, data)
            self.assertTrue(resp.context['form'].errors.has_key(key))

    def testPostNewCommentFail(self):
        data = self.get_valid_post_data()
        data.pop('content')
        
        resp = self.client.post(self.url, data)
        cntx = resp.context

        self.assertEquals(200, resp.status_code)
        self.assertFalse(cntx.get('success'))
        self.assertTrue(isinstance(cntx.get('form'), CommentForm))
        self.assertTrue(cntx.get('comment') is None)

# --------------------------------------------------------------------------- #

class ReplyCommentTest(BaseCommentTest):
    def get_view_name(self):
        return 'comments_reply'

        


