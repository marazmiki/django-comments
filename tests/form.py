# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from comments.forms import CommentForm
from comments.tests import get_content_object

class FormTest(TestCase):
    def testWrongKwarg(self):
        def do_wrong():
            CommentForm(foo='bar')
        self.assertRaises(TypeError, do_wrong)
        
    def testObjectKwarg(self):
        object = get_content_object()
        form   = CommentForm(object=object)
        self.assertEquals(ContentType.objects.get_for_model(object).pk, form.initial.get('content_type'))
        self.assertEquals(object.pk, form.initial.get('object_pk'))