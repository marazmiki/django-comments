# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment, LastReadedComment
from comments.managers import CommentManager, LastReadedCommentManager
from comments.tests import create_comment, get_content_object, create_user
from comments.query import CommentsQuerySet, LastReadedCommentQuerySet

# --------------------------------------------------------------------------- #

class CommentManagerTest(TestCase):
    def setUp(self):
        self.comment = create_comment()
        self.object = get_content_object()

    def testQuerySetInstance(self):
        self.assertTrue(isinstance(Comment.objects.all(), CommentsQuerySet))

    def testInstance(self):
        self.assertTrue(isinstance(Comment.objects, CommentManager))

    def testGetForObject(self):
        another_ctype_id = 2
        another_object   = get_content_object(another_ctype_id)
        comments_number  = 3

        for i in xrange(comments_number):
            create_comment(another_ctype_id)

        self.assertEquals(1,                   Comment.objects.get_for_object(self.object).count())
        self.assertEquals(comments_number,     Comment.objects.get_for_object(another_object).count())
        self.assertEquals(comments_number + 1, Comment.objects.count())


    def testApprovedFilter(self):
        qset = Comment.objects.get_for_object(self.object)
        self.assertEquals(1, qset.count())
        
        # Create unapproved comment
        comment = create_comment()
        comment.is_approved=False
        comment.save()
        
        self.assertEquals(1, qset.approved().count())
        self.assertEquals(2, Comment.objects.count())

# --------------------------------------------------------------------------- #

class LastReadedCommentManagerTest(TestCase):
    def setUp(self):
        self.comment = create_comment()
        self.object = get_content_object()
        self.user = create_user()

    def testQuerySetInstance(self):
        self.assertTrue(isinstance(LastReadedComment.objects.all(), LastReadedCommentQuerySet))

    def testInstance(self):
        self.assertTrue(isinstance(LastReadedComment.objects, LastReadedCommentManager))

    def testGetForUserAndObject(self):
        LastReadedComment.objects.create(
            user    = self.user,
            comment = self.comment,
            content_object  = self.object,
        )

        last_readed = LastReadedComment.objects.get_for_user_and_object(
            user           = self.user,
            content_object = self.object,
        )

        self.assertTrue(isinstance(last_readed, LastReadedComment))
        self.assertEquals(self.comment, last_readed.comment)
        self.assertEquals(self.user, last_readed.user)
        self.assertEquals(unicode(self.comment), unicode(last_readed))


    def testGetForUserAndObjectIfNone(self):
        old_data = LastReadedComment.objects.all()
        old_data.delete()

        last_readed = LastReadedComment.objects.get_for_user_and_object(
            user           = self.user,
            content_object = self.object,
        )

        self.assertTrue(last_readed is None)
