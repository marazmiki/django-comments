# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template import Template, Context, TemplateSyntaxError
from django.core.urlresolvers import reverse
from reusable.comments.tests import TestCase, CommentViewTest, views

# --------------------------------------------------------------------------- #

class CommentsFormActionTestCase(CommentViewTest):    
    """    
    Примеры правильных вызовов тега

    {% comment_form_action %}   
    {% comment_form_action as [form_action] %} 
    {% comment_form_action for schema [schema] %} 
    {% comment_form_action for schema [schema] as [form_action] %} 
    """ 
    def test_template_error_if_wrong_arg_number(self):
        """
        Первое условие парсера: сообщать о неверном количестве аргументов,
        если размер bits не равен 1, 3, 4 или 6
        """
        missing_tags = [
            '{% comment_form_action as %}',                          # 2 
            '{% comment_form_action for schema foo bar %}',          # 5
            '{% comment_form_action for schema foo bar baz baz %}',  # 7
        ]
 
        for mt in missing_tags:
            self.assertRaises(TemplateSyntaxError, lambda: self.render(mt,{}))

    def test_success_if_first_keyword_is_as(self):
        """
        Проверяет, что если в параметрах тега первый аргумент - ключевое
        слово "as", ошибка не возникает
        """
        self.render('{% comment_form_action as "varname" %}', {})

    def test_success_if_keyword_are_for_schema(self):
        """
        Проверяет, что если в параметрах тега первый аргумент - ключевое
        слово "for", а второе - "schema", ошибка не возникает
        """
        self.render('{% comment_form_action for schema "default" %}', {})

    def test_success_all_args(self):
        """
        Проверяет, что если все параметры тега указаны, синтаксической
        ошибки не возникает
        """
        self.render(
            '{% comment_form_action for schema "default" as varname %}', 
            {'varname': 'form_action'},
        )


    def test_fail_if_first_keyword_is_for_but_second_is_not_schema(self):
        """
        Проверяет, что если в параметрах тега первый аргумент - ключевое
        слово "for", а второе - не "schema", возникает ошибка синтаксиса
        """
        self.assertRaises(
            TemplateSyntaxError,
            lambda: self.render('{% comment_form_action for sch3ma "default" %}', {})
        )

    def test_fail_if_first_keyword_not_as_and_not_for(self):
        """
        Проверяет, что если в параметрах тега первый аргумент не является
        ключевым словом "for" или "as", возникает ошибка синтаксиса
        """
        self.assertRaises(
            TemplateSyntaxError,
            lambda: self.render('{% comment_form_action blah "default" %}', {})
        )

    def test_fail_if_scheme_specified_mut_varname_empty(self):
        """
        Проверяет, что если в параметрах тега явно указана схема (for scheme),
        и присутствует ключевое слово 'as', но его значение не указано,
        возникает ошибка синтаксиса          
        """
        self.assertRaises(
            TemplateSyntaxError,
            lambda: self.render(
                '{% comment_form_action for schema "default" as %}', 
                dict(varname='form_action'),
            )
        )

    def test_fail_if_scheme_specified_mut_varname_empty2(self):
        """
        Проверяет, что если в параметрах тега явно указана схема (for schema),
        и присутствует ключевое слово 'as', но его значение не указано,
        возникает ошибка синтаксиса          
        """
        self.assertRaises(
            TemplateSyntaxError,
            lambda: self.render(
                '{% comment_form_action for schema "default" a5 "var" %}', 
                dict(varname='form_action'),
            )
        )
