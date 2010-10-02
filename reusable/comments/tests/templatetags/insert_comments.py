# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template import Template, Context, TemplateSyntaxError
from django.core.urlresolvers import reverse
from reusable.comments.tests import TestCase, CommentViewTest, views, models

class InsertCommentsTestCase(CommentViewTest):    
    """ 
    {% insert_comments for [object] %}
    {% insert_comments for [object] with schema [schema] %}
    """
    urls = 'reusable.comments.tests.urls'
    view_name = 'test_view_insert_comment_brief'
       
    def test_syntax_ok_brief(self):
        resp = self.get()        
        self.assertEquals(200, resp.status_code)      

    def test_syntax_ok_full(self):        
        self.view_name = 'test_view_insert_comment_full'
        resp = self.get()
        self.assertEquals(200, resp.status_code)

    def test_syntax_wrong(self):
        """
        Проверяет, генерируется ли исключение TemplateSyntaxError, если
        тег вызывается синтаксически некорректно
        """
        templates = [
            '{% insert_comments f0r object %}',
            '{% insert_comments for %}',
            '{% insert_comments for object with %}',
            '{% insert_comments for object w1th %}',            
            '{% insert_comments for object with schema %}',
            '{% insert_comments for object with sch3ma schema %}',
            '{% insert_comments for object with schema foo bar %}',            
        ]

        for template in templates:
            def raise_error():
                Template(template).render(Context({'object':None}))           

            self.assertRaises(TemplateSyntaxError, raise_error)
                