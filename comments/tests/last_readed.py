# -*- coding: utf-8 -*-

from django.test import TestCase, client
from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType
from comments.tests import create_user, create_comment, get_content_object, USERNAME, PASSWORD
from comments.models import Comment, LastReadedComment

class LastReadedTest(TestCase):
    urls = 'comments.tests.urls'

    def setUp(self):
        self.user_john = create_user(USERNAME)
        self.user_jane = create_user('john')
        self.object = get_content_object()
        self.client = client.Client()
        self.auth()

    def auth(self):
        assert self.client.login(
            username=USERNAME,
            password=PASSWORD,
        )

    def testSaveLastReadedForAuthUser(self):
        comment = create_comment()

        self.assertEquals(0, LastReadedComment.objects.count())
        self.client.get(urlresolvers.reverse('templatetags_insert_comment'))
        self.assertEquals(
            comment,
            LastReadedComment.objects.get_for_user_and_object(
                user=self.user_john,
                content_object = self.object
            ).comment
        )

    def testSaveLastReadedForAuthUserChangeState(self):
        comment = create_comment()
        self.assertEquals(0, LastReadedComment.objects.count())
        
        self.client.get(urlresolvers.reverse('templatetags_insert_comment'))
        self.assertEquals(1, LastReadedComment.objects.count())
        self.assertEquals(comment,
            LastReadedComment.objects.get_for_user_and_object(
                user=self.user_john,
                content_object = self.object
            ).comment
        )

        comment_new = create_comment()
        comment_new.content += '!!!!!'
        comment_new.save()

        self.client.get(urlresolvers.reverse('templatetags_insert_comment'))

        self.assertEquals(1, LastReadedComment.objects.count())
        self.assertEquals(2, Comment.objects.get_for_object(self.object).count())
        self.assertEquals(
            comment_new,
            LastReadedComment.objects.get_for_user_and_object(
                user=self.user_john,
                content_object = self.object
            ).comment
        )

    def testNotSaveLastReadedForGuestUser(self):
        self.client.logout()
        comment = create_comment()

        self.assertEquals(0, LastReadedComment.objects.count())
        self.client.get(urlresolvers.reverse('templatetags_insert_comment'))
        self.assertTrue(
            LastReadedComment.objects.get_for_user_and_object(
                user           = self.user_john,
                content_object = self.object
            ) is None
        )


    def testCreateCommentAndMarksAsReaded(self):
        qset = Comment.objects.get_for_object(self.object)
        
        self.assertEquals(0, LastReadedComment.objects.count())
        self.assertEquals(0, qset.count())

        self.client.post(
            urlresolvers.reverse('comments_create'),
            dict(
                content = 'Hello world',
                object_pk = self.object.pk,
                content_type = ContentType.objects.get_for_model(self.object).pk,
            )
        )

        self.assertEquals(1, qset.count())
        self.assertEquals(qset[0],
            LastReadedComment.objects.get_for_user_and_object(
                user=self.user_john,
                content_object = self.object
            ).comment
        )


    def testGuestCreateCommentAndMarksAsReaded(self):
        qset = Comment.objects.get_for_object(self.object)

        self.assertEquals(0, LastReadedComment.objects.count())
        self.assertEquals(0, qset.count())

        self.client.logout()
        self.client.post(
            urlresolvers.reverse('comments_create'),
            dict(
                content = 'Hello world',
                object_pk = self.object.pk,
                content_type = ContentType.objects.get_for_model(self.object).pk,
            )
        )

        self.assertEquals(1, qset.count())
        self.assertTrue(
            LastReadedComment.objects.get_for_user_and_object(
                user=self.user_john,
                content_object = self.object
            ) is None
        )
