# -*- coding: utf-8 -*-

from django.db.models import Model
from django.template import Library, Node, Variable, TemplateSyntaxError
from django.template.loader import render_to_string

register = Library()

# --------------------------------------------------------------------------- #

class InsertCommentsNode(Node):
    def __init__(self, object):
        self.object = Variable(object)

    def render(self, context):
        object = self.object.resolve(context) if self.object else None

        if object and isinstance(object, Model):
            context.update({'object':object})
            return render_to_string('comments/insert_comments.html', context)

        else:
            return ''

# --------------------------------------------------------------------------- #

@register.tag
def insert_comments(parser, token):
    bits = token.split_contents()

    if len(bits) != 3 or bits[1].lower() != 'for':
        raise TemplateSyntaxError(
            "Wrong syntax for '%(tag)s'. Use {%% %(tag)s for [obj] %%} " % dict(
                tag = bits[0],
            )
        )

    return InsertCommentsNode(object=bits[2])