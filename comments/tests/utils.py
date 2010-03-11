# -*- coding: utf-8 -*-

from django.test import TestCase
from comments.models import Comment, LastReadedComment
from comments.utils import count_comments_for_object, count_unreaded_comments
from comments.tests import get_content_object, create_comment, create_user

class UtilTest(TestCase):
    def setUp(self):
        self.object = get_content_object()

    def test_get_count_comment_for_object(self):
        for i in xrange(0, 3):
            create_comment()
            self.assertEquals(i+1, count_comments_for_object(self.object))
            
    def test_get_count_comment_for_object_not_approved(self):
        num_comments = 3
        self.assertEquals(0, count_comments_for_object(self.object))

        for i in xrange(0, num_comments):
            comment, comment_bad = create_comment(), create_comment()
            comment_bad.is_approved = False
            comment_bad.save()

        self.assertEquals(num_comments * 2, Comment.objects.get_for_object(self.object).count())
        self.assertEquals(num_comments, Comment.objects.get_for_object(self.object).approved().count())
        self.assertEquals(
            Comment.objects.get_for_object(self.object).approved().count(),
            count_comments_for_object(self.object)
        )


class CountUnreadCommentsTest(TestCase):
    def setUp(self):
        self.object = get_content_object()
        self.john   = create_user('John')
        self.jane   = create_user('Jane')
        self.fred   = create_user('Fred')

        self.comment_old = create_comment()
        self.comment_new = create_comment()

    def test_comment_eq_0_when_all_comments_is_readed(self):
        LastReadedComment.objects.create(
            user    = self.john,
            comment = self.comment_new,
            content_object = self.object,
        )

        self.assertEquals(2, Comment.objects.get_for_object(self.object).count())
        self.assertEquals(0, count_unreaded_comments(self.object, self.john))

    def test_when_unread_not_equal_count(self):
        LastReadedComment.objects.create(
            user    = self.jane,
            comment = self.comment_old,
            content_object = self.object,
        )

        self.assertEquals(2, Comment.objects.get_for_object(self.object).count())
        self.assertEquals(1, count_unreaded_comments(self.object, self.jane))

    def test_count_eq_unreaded_count_if_no_lrc_found(self):
        self.assertEquals(2, Comment.objects.get_for_object(self.object).count())
        self.assertEquals(
            count_comments_for_object(self.object),
            count_unreaded_comments(self.object, self.fred)
        )