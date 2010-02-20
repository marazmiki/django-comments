# -*- coding: utf-8 -*-

from django.db.models import Model
from django.core import urlresolvers
from django.template import Library, Node, Variable, TemplateSyntaxError
from django.template.loader import render_to_string
from comments.models import Comment

register = Library()

# --------------------------------------------------------------------------- #

class InsertCommentsNode(Node):
    def __init__(self, object):
        self.object = Variable(object)

    def render(self, context):
        object = self.object.resolve(context) if self.object else None

        if object and isinstance(object, Model):
            context.update({
                'object'           : object,
                'comments_enabled' : True,   # TODO: get this setting
            })

            return render_to_string('comments/insert_comments.html', context)

        else:
            return ''
# --------------------------------------------------------------------------- #

class CommentsFormActionNode(Node):
    def __init__(self, object=None, parent=None):
        self.object = Variable(object) if object else None
        self.parent = Variable(parent) if parent else None

    def render(self, context):
        object = self.object.resolve(context) if self.object else None
        parent = self.parent.resolve(context) if self.parent else None

        if parent and isinstance(parent, Comment):
            return urlresolvers.reverse('comments_reply',
                kwargs = {
                    'parent_id': parent.pk,
                }
            )

        return urlresolvers.reverse('comments_create')

# --------------------------------------------------------------------------- #

class CommentsListNode(Node):
    def __init__(self, object, varname):
        self.object = Variable(object)
        self.varname = varname

    def render(self, context):
        object = self.object.resolve(context)
        context[self.varname] = Comment.objects.get_for_object(object)
        return ''
    
# --------------------------------------------------------------------------- #

@register.tag
def insert_comments(parser, token):
    bits = token.split_contents()

    if len(bits) != 3 or bits[1] != 'for':
        raise TemplateSyntaxError(
            "Wrong syntax for '%(tag)s'. Use {%% %(tag)s for [obj] %%} " % dict(
                tag = bits[0],
            )
        )

    return InsertCommentsNode(object=bits[2])
    
# --------------------------------------------------------------------------- #

@register.tag
def comments_form_action(parser, token):
    """

    {% comments_form_action %}
    {% comments_form_action for [object] %}
    {% comments_form_action in reply to [parent] %}
    {% comments_form_action for [object] in reply to [parent] %}

    """
    tokens = token.split_contents()
    object, parent = None, None
    length, errors = len(tokens), True

    if length is 1:
        errors = False

    elif length is 3 and tokens[1] == 'for':
        errors = False
        object = tokens[2]

    elif length is 5 and tokens[1] == 'in' and tokens[2] == 'reply' and \
        tokens[3] == 'to':
        errors = False
        parent = tokens[4]

    elif length is 7 and tokens[1] == 'for' and tokens[3] == 'in' and \
        tokens[4] == 'reply' and tokens[5] == 'to':
        errors = False
        parent = tokens[6]
        object = tokens[2]

    if errors:
        raise TemplateSyntaxError('Wrong syntax for %s tag' % tokens[0])

    return CommentsFormActionNode(object=object, parent=parent)
    
# --------------------------------------------------------------------------- #

@register.tag
def get_comments_list(parser, token):
    tokens = token.split_contents()
    length = len(tokens)

    if length is not 5 or tokens[1] != 'for' or tokens[3] != 'as':
        raise TemplateSyntaxError(
            '{%% %s for [object] as [varname] %%}' % tokens[0]
        )

    return CommentsListNode(object=tokens[2], varname=tokens[4])
