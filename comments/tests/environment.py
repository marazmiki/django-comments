# -*- coding: utf-8 -*-

from django.test import TestCase
from django.conf import settings

class EnvironmentTest(TestCase):
    def test_context_processor_request(self):
        self.assertTrue(
            'django.core.context_processors.request' in settings.TEMPLATE_CONTEXT_PROCESSORS
        )

    def test_context_processor_media(self):
        self.assertTrue(
            'django.core.context_processors.media' in settings.TEMPLATE_CONTEXT_PROCESSORS
        )

