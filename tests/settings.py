# -*- coding: utf-8 -*-

from django.test import TestCase
from comments.models import Comment, CommentSettings
from comments.settings import PREMODERATE, ENABLED, LEVEL_LIMIT
from comments.tests import get_content_object, create_comment

class SettingsTest(TestCase):
    def setUp(self):
        to_delete = CommentSettings.objects.all()
        to_delete.delete()
        
        self.object = get_content_object()
        self.comment = create_comment()

    def testInstance(self):
        self.assertTrue(isinstance(self.comment.get_settings(), CommentSettings))

    def testDefaultSettings(self):
        comment_settings = self.comment.get_settings()
        
        self.assertEquals(PREMODERATE, comment_settings.premoderate)
        self.assertEquals(ENABLED,     comment_settings.enabled)
        self.assertEquals(LEVEL_LIMIT, comment_settings.level_limit)

    def testOverrideSettings(self):
        c = CommentSettings.objects.create(
            premoderate    = not PREMODERATE,
            enabled        = not ENABLED,
            level_limit    = LEVEL_LIMIT + 15,
            content_object = self.object,
        )
        c.save()

        comment_settings = self.comment.get_settings()

        self.assertEquals(not PREMODERATE,  comment_settings.premoderate)
        self.assertEquals(not ENABLED,      comment_settings.enabled)
        self.assertEquals(LEVEL_LIMIT + 15, comment_settings.level_limit)
        
    # TODO: test level_limit
    