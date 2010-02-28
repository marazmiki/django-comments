# -*- coding: utf-8 -*-

from django.test import TestCase
from comments.models import Comment
from comments.utils import count_comments_for_object
from comments.tests import get_content_object, create_comment

class UtilTest(TestCase):
    def setUp(self):
        self.object = get_content_object()

    def testGetCountCommentForObject(self):
        for i in xrange(0, 3):
            create_comment()
            self.assertEquals(i+1, count_comments_for_object(self.object))
            
    def testGetCountCommentForObjectNotApproved(self):
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