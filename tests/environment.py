# -*- coding: utf-8 -*-

from django.test import TestCase
from django.conf import settings

class EnvironmenTest(TestCase):
    def testContextProcessorRequest(self):
        self.assertTrue(
            'django.core.context_processors.request' in settings.TEMPLATE_CONTEXT_PROCESSORS
        )

    def testContextProcessorMedia(self):
        self.assertTrue(
            'django.core.context_processors.media' in settings.TEMPLATE_CONTEXT_PROCESSORS
        )

