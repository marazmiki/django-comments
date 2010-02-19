# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment
from comments.managers import CommentManager
from comments.tests import create_comment, get_content_object

# --------------------------------------------------------------------------- #

class CommentManagerTest(TestCase):
    def setUp(self):
        self.comment = create_comment()
        self.object = get_content_object()

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
        
