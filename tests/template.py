# -*- coding: utf-8 -*-

from django.test import TestCase, client
from django.template import Template, Context, add_to_builtins, TemplateSyntaxError
from comments.tests import get_commentable_object

# --------------------------------------------------------------------------- #

add_to_builtins('django.templatetags.i18n')
add_to_builtins('comments.templatetags.comments_tags')

# --------------------------------------------------------------------------- #

class BaseTestCase(TestCase):
    def setUp(self):
        self.tpl_string  = self.get_valid_tag_template()
        self.tpl_context = dict(object=get_commentable_object())

    def render(self):
        t = Template(self.tpl_string)
        c = Context(self.tpl_context)
        return t.render(c)

    def get_valid_tag_template(self):
        raise NotImplementedError('Please implement this method in your suite')

# --------------------------------------------------------------------------- #

class CommentsTagTest(BaseTestCase):
    def get_valid_tag_template(self):
        return '{% insert_comments for object %}'

    def testCorrect(self):
        self.render()

    def testEmptyObject(self):
        self.tpl_context.update({'object': None})
        self.assertEquals('', self.render())

    def testEmptyObject2(self):
        self.tpl_context.update({'object': 'asdas'})
        self.assertEquals('', self.render())


    def testNodeWrongFirstArg(self):
        def do_wrong():
            self.tpl_string = '{% insert_comments f0r object %}'
            self.render()

        self.assertRaises(TemplateSyntaxError, do_wrong)

    def testNodeWrongNumberOfArgs(self):
        def do_wrong():
            self.tpl_string = '{% insert_comments for object something %}'
            self.render()

        self.assertRaises(TemplateSyntaxError, do_wrong)

    def testNodeWrongNumberOfArgs(self):
        def do_wrong():
            self.tpl_string = '{% insert_comments for object something %}'
            self.render()

        self.assertRaises(TemplateSyntaxError, do_wrong)
