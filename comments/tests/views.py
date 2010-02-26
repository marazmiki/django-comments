# -*- coding: utf-8 -*-

from django.test import TestCase, client
from django.core import urlresolvers, exceptions
from django.contrib.contenttypes.models import ContentType
from django.utils import simplejson
from comments.forms import CommentForm, ReplyForm
from comments.models import Comment, CommentSettings
from comments.tests import get_content_object, create_comment
from comments.settings import PREMODERATE

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
        args, kwargs = self.get_view_args()

        if view:
            return urlresolvers.reverse(view, args=args, kwargs=kwargs)

    def get_view_name(self):
        return None

    def get_view_args(self):
        return None, None
# --------------------------------------------------------------------------- #

class CreateCommentTest(BaseCommentTest):
    def setUp(self):
        super(CreateCommentTest, self).setUp()
        self.object = get_content_object()

    def get_valid_post_data(self):
        return dict(
            content = 'Hello world',
            object_pk    = self.object.pk,
            content_type = ContentType.objects.get_for_model(self.object).pk,
        )

    def get_view_name(self):
        return 'comments_create'

    def testCreateCommentToUncommentable(self):
        cs = CommentSettings.objects.create(
            content_object = self.object,
            enabled = False,
        )

        data = self.get_valid_post_data()
        resp = self.client.post(self.url, data)
        self.assertEquals(404, resp.status_code)

    def testCreateCommentToPremoderate(self):
        cs   = CommentSettings.objects.create(content_object = self.object)
        data = self.get_valid_post_data()

        for flag in [True, False]:
            # Clean all comments
            to_delete = Comment.objects.all()
            to_delete.delete()
            self.assertEquals(0, Comment.objects.get_for_object(self.object).count())

            # If premoderate is True then isapproved is False and vice versa
            cs.premoderate = not flag
            cs.save()

            # Create comment and check flag
            self.client.post(self.url, data)

            if flag:
                self.assertTrue(Comment.objects.get_for_object(self.object)[0].is_approved)
            else:
                self.assertEquals(0, Comment.objects.get_for_object(self.object).approved().count())
                self.assertEquals(0, Comment.objects.approved().get_for_object(self.object).count())

    def testCreateViewExists(self):
        data = self.get_valid_post_data()
        resp = self.client.post(self.url, data)
        self.assertEquals(302, resp.status_code)

    def testTemplateName(self):
        data = self.get_valid_post_data()
        data.pop('content', None)

        resp = self.client.post(self.url, data)
        tmpl = 'comments/create.html'

        if isinstance(resp.template, list):
            self.assertEquals(tmpl, resp.template[0].name)
        else:
            self.assertEquals(tmpl, resp.template.name)

    def testFormInTemplateContext(self):
        data = self.get_valid_post_data()
        data.pop('content', None)

        resp = self.client.post(self.url, data)
        cntx = resp.context[0]

        self.assertTrue(isinstance(cntx.get('form'), CommentForm))

    def testPostNewCommentSuccess(self):
        resp = self.client.post(self.url, self.get_valid_post_data())
        self.assertEquals(302, resp.status_code)

    def testPostNewCommentSuccessRedirect(self):
        page  = '/foo/bar/'
        state = ('http://testserver' + page, 302)

        data = self.get_valid_post_data()
        data.update(redirect_to=page)

        resp  = self.client.post(self.url, data, follow=True, HTTP_REFERER=state[0])
        self.assertTrue(state in resp.redirect_chain)

    def testPostNewCommentSuccessRedirectImplicitGiven(self):
        resp = self.client.post(self.url, self.get_valid_post_data(),follow=True)
        self.assertTrue(('http://testserver/', 302) in resp.redirect_chain)

    def testAjaxPostNewCommentSuccess(self):
        resp = self.client.post(self.url, self.get_valid_post_data(), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        json = simplejson.loads(resp.content)

        self.assertEquals(200, resp.status_code)
        self.assertTrue(json.has_key('success'))
        self.assertTrue(json.has_key('comment'))
        self.assertTrue(json.has_key('parent_id'))
        self.assertTrue(json.get('parent_id') is None)
        self.assertTrue(json.get('success'))

    def testPostNewCommentFailEachField(self):
        data = self.get_valid_post_data()

        for key, value in data.items():
            # We can't delete object_pk and content_type fields because it
            # raises 404 error
            if key in ['object_pk', 'content_type']:
                continue

            del data[key]
            resp = self.client.post(self.url, data)

            self.assertTrue(resp.context['form'].errors.has_key(key))
            self.assertFalse(resp.context['success'])

    def testAjaxPostNewCommentFailEachField(self):
        data = self.get_valid_post_data()

        for key, value in data.items():
            # We can't delete object_pk and content_type fields because it
            # raises 404 error
            if key in ['object_pk', 'content_type']:
                continue

            del data[key]
            resp = self.client.post(self.url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            json = simplejson.loads(resp.content)
            self.assertFalse(json['success'])
            self.assertTrue(json['errors'].has_key(key))

    def testPostNewCommentFail(self):
        data = self.get_valid_post_data()
        data.pop('content')

        resp = self.client.post(self.url, data)
        cntx = resp.context[0]

        self.assertEquals(200, resp.status_code)
        self.assertFalse(cntx.get('success'))
        self.assertTrue(isinstance(cntx.get('form'), CommentForm))
        self.assertTrue(cntx.get('comment') is None)

    def testCreateWrongContentObject(self):
        data = self.get_valid_post_data()
        data.update(
            object_pk    = 666,
            content_type = 999,
        )

        resp = self.client.post(self.url, data)
        self.assertEquals(404, resp.status_code)

# --------------------------------------------------------------------------- #

class ReplyCommentTest(BaseCommentTest):
    def get_view_name(self):
        return 'comments_reply'

    def get_view_args(self):
        return None, {'parent_id': self.parent.pk,}

    def get_valid_post_data(self):
        return dict(
            content = 'Reply to comment #1'
        )
    
    def setUp(self):
        self.object = get_content_object()
        self.parent = create_comment()
        super(ReplyCommentTest, self).setUp()

    def testReplyCommentToUncommentable(self):
        cs = CommentSettings.objects.create(
            content_object = self.object,
            enabled = False,
        )

        data = self.get_valid_post_data()
        resp = self.client.post(self.url, data)
        self.assertEquals(404, resp.status_code)


    def testReplyViewExists(self):
        resp = self.client.get(self.url)
        cntx = resp.context[0]
        self.assertEquals(200, resp.status_code)
        self.assertEquals(cntx.get('object'), self.object)
        self.assertEquals(cntx.get('parent'), self.parent)
        self.assertTrue(isinstance(cntx.get('form'), CommentForm))

    def testReplyCreateSuccess(self):
        resp = self.client.post(self.url, self.get_valid_post_data())
        self.assertEquals(302, resp.status_code)
        self.assertEquals(2, Comment.objects.get_for_object(self.object).count())

    def testAjaxReplyCreateSuccess(self):
        resp = self.client.post(self.url, self.get_valid_post_data(), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        json = simplejson.loads(resp.content)

        self.assertEquals(200, resp.status_code)
        self.assertEquals(2, Comment.objects.get_for_object(self.object).count())
        self.assertTrue(json.has_key('comment'))
        self.assertTrue(json.has_key('parent_id'))
        self.assertTrue(json.get('parent_id'), self.parent.pk)
        self.assertTrue(isinstance(json.get('comment'), basestring))

    def testReplyCreateFail(self):
        data = self.get_valid_post_data()

        for key, value in data.items():
            del data[key]
            resp = self.client.post(self.url, data)
            self.assertTrue(resp.context['form'].errors.has_key(key))

        self.assertEquals(1, Comment.objects.get_for_object(self.object).count())

    def testAjaxReplyCreateFail(self):
        data = self.get_valid_post_data()

        for key, value in data.items():
            del data[key]
            resp = self.client.post(self.url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            json = simplejson.loads(resp.content)
            self.assertTrue(json['errors'].has_key(key))

        self.assertEquals(1, Comment.objects.get_for_object(self.object).count())
        
    def testReplyCommentToPremoderate(self):
        cs   = CommentSettings.objects.create(content_object = self.object)
        qs   = Comment.objects.get_for_object(self.object).filter(level__gt=0)
        data = self.get_valid_post_data()

        for flag in [True, False]:
            # Clean all comments
            to_delete = qs
            to_delete.delete()

            # If premoderate is True then isapproved is False and vice versa
            cs.premoderate = not flag
            cs.save()

            # Create comment and check flag
            self.client.post(self.url, data)

            if flag:
                self.assertTrue(qs[0].is_approved)
            else:
                self.assertEquals(0, qs.approved().count())