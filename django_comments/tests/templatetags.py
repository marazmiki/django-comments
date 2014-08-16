# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import test
from django.template import Template, Context, TemplateSyntaxError


class TemplateTagTest(test.TestCase):
    def setUp(self):
        pass

    def render(self, string, context={}):
        ctx = Context(context)
        return Template('{% load comments_tags %}' + string).render(ctx)

    def test_no_args(self):
        self.render('{% insert_comments %}')

    def test_one_arg_content_object(self):
        self.render('{% insert_comments obj %}', {'obj': None})

    def test_one_arg_for_raise(self):
        self.assertRaises(TemplateSyntaxError,
                          lambda: self.render('{% insert_comments for %}'))

    def test_two_args(self):
        self.render('{% insert_comments for obj %}', {'obj': None})

    def test_three_args_last_with_raise(self):
        self.assertRaises(TemplateSyntaxError,
                          lambda: self.render('{% insert_comments for obj with', {'obj': None}))
