# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import template


register = template.Library()


class InsertCommentsNode(template.Node):
    """
    """
    def __init__(self, *args, **kwargs):
        pass

    def render(self, context):
        return ''


@register.tag
def insert_comments(parser, token):
    """
    Insert comments widget into page

    {% insert_comments %}
    {% insert_comments content_object %}
    {% insert_comments for content_object with template_name='' %}
    """
    bits = token.split_contents()
    length = len(bits)

    if length == 1:
        'Case: {% insert_comments %}'
    elif length == '2':
        'Case: {% insert_comments content_object %}'
        if bits[1].lower() == 'for':
            raise template.TemplateSyntaxError("If you're specify the `for` "
                                               "argument, you must specify "
                                               "also `content_object` 3rd "
                                               "argument")
    elif length >= 3:
        'Case: {% insert_comments for content_object %}'
        if length == 4 and bits[3].lower() == 'with':
            raise template.TemplateSyntaxError("")
    return InsertCommentsNode()