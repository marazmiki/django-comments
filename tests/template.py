# -*- coding: utf-8 -*-

from django.test import TestCase, client
from django.core import urlresolvers
from django.template import Template, Context, add_to_builtins, TemplateSyntaxError
from comments.tests import get_content_object, create_comment
from comments.models import Comment

# --------------------------------------------------------------------------- #

add_to_builtins('django.templatetags.i18n')
add_to_builtins('comments.templatetags.comments_tags')

# --------------------------------------------------------------------------- #

class BaseTestCase(TestCase):
    def setUp(self):
        self.tpl_string  = self.get_valid_tag_template()
        self.tpl_context = dict(object=get_content_object())

    def render(self):
        self.t = Template(self.tpl_string)
        self.c = Context(self.tpl_context)
        return self.t.render(self.c)

    def get_valid_tag_template(self):
        raise NotImplementedError('Please implement this method in your suite')

# --------------------------------------------------------------------------- #

class InsertCommentsTagTest(BaseTestCase):
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

# --------------------------------------------------------------------------- #

class CommentsFormActionTagTest(BaseTestCase):
    def get_valid_tag_template(self):
        return '{% comments_form_action %}'

    def create_action(self):
        return urlresolvers.reverse('comments_create')

    def reply_action(self):
        return urlresolvers.reverse('comments_reply',
            kwargs = {
                'parent_id': self.tpl_context['parent'].pk
            }
        )

    def testCommentAddAsIs(self):
        self.assertEquals(self.create_action(), self.render())

    def testCommentAddForObject(self):
        self.tpl_string = '{% comments_form_action for object %}'
        self.assertEquals(self.create_action(), self.render())

    def testCommentAddForObjectInEmptyReply(self):
        self.tpl_string = '{% comments_form_action for object in reply to parent %}'
        self.tpl_context.update(parent=None)
        self.assertEquals(self.create_action(), self.render())

    def testCommentReplyToParent(self):
        self.tpl_string  = '{% comments_form_action in reply to parent %}'
        self.tpl_context.update(parent=create_comment())
        self.assertEquals(self.reply_action(), self.render())

    def testCommentReplyForObject(self):
        self.tpl_string = '{% comments_form_action for object in reply to parent %}'
        self.tpl_context.update(parent=create_comment())
        self.assertEquals(self.reply_action(), self.render())
        
    def testSyntaxErrorsWrongArgsNum(self):
        def do_wrong():
            self.tpl_string = '{% comments_form_action for %}'
            self.render()
        self.assertRaises(TemplateSyntaxError, do_wrong)
        
# --------------------------------------------------------------------------- #

class CommentsListTagTest(BaseTestCase):
    def get_valid_tag_template(self):
        return '{% get_comments_list for object as var %}'

    def testSyntaxOk(self):
        html = self.render()

    def testSyntaxErrorsWrongArgsNum(self):
        def do_wrong():
            self.tpl_string = '{% get_comments_list blah %}'
            self.render()
        self.assertRaises(TemplateSyntaxError, do_wrong)

    def testSyntaxErrorsSecondArgIsNotFor(self):
        def do_wrong():
            self.tpl_string = '{% get_comments_list for_ object as var %}'
            self.render()
        self.assertRaises(TemplateSyntaxError, do_wrong)

    def testSyntaxErrorsThirdArgIsNotAs(self):
        def do_wrong():
            self.tpl_string = '{% get_comments_list for object a$ var %}'
            self.render()
        self.assertRaises(TemplateSyntaxError, do_wrong)
