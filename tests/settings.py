# -*- coding: utf-8 -*-

from django.test import TestCase
from comments.models import Comment, CommentSettings
from comments.settings import PREMODERATE, ENABLED, LEVEL_LIMIT
from comments.utils import get_settings_for_object
from comments.tests import get_content_object, create_comment

class SettingsTest(TestCase):
    def setUp(self):
        self.object   = get_content_object()
        self.comment  = create_comment()
        self.settings = CommentSettings.objects.create(
            premoderate    = not PREMODERATE,
            enabled        = not ENABLED,
            level_limit    = LEVEL_LIMIT + 15,
            content_object = self.object,
        )

    def testInstance(self):
        self.assertTrue(
            isinstance(get_settings_for_object(self.object), CommentSettings)
        )

    def testDefaultSettings(self):
        to_delete = CommentSettings.objects.all()
        to_delete.delete()

        comment_settings = get_settings_for_object(self.object)
        
        self.assertEquals(PREMODERATE, comment_settings.premoderate)
        self.assertEquals(ENABLED,     comment_settings.enabled)
        self.assertEquals(LEVEL_LIMIT, comment_settings.level_limit)

    def testUnicode(self):
        self.assertEquals(
            unicode(self.object),
            unicode(get_settings_for_object(self.object))
        )

    def testOverrideSettings(self):

        comment_settings = get_settings_for_object(self.object)

        self.assertEquals(not PREMODERATE,  comment_settings.premoderate)
        self.assertEquals(not ENABLED,      comment_settings.enabled)
        self.assertEquals(LEVEL_LIMIT + 15, comment_settings.level_limit)
        
    # TODO: test level_limit
    