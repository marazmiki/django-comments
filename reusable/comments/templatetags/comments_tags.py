# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.template import Node, Library, Variable, TemplateSyntaxError, RequestContext
from django.template.loader import render_to_string
from reusable.comments.plugins import get_plugin

# --------------------------------------------------------------------------- #

register = Library()

# --------------------------------------------------------------------------- #

class InsertCommentsNode(Node):
    def __init__(self, object=object, schema=None):
        self.object = Variable(object)
        self.schema = Variable(schema) if schema else None       

    def render(self, context):
        schema = self.schema.resolve(context) if self.schema else None
        object = self.object.resolve(context)
        ctype  = ContentType.objects.get_for_model(object)

        request = context['request'] 
        plugin  = get_plugin(schema)

        return render_to_string(
            (
                'comments_plugins/%s/%s/%s/insert_comments.html' % (schema, ctype.app_label, ctype.model,),
                'comments_plugins/%s/%s/insert_comments.html' % (schema, ctype.model,),
                'comments_plugins/%s/insert_comments.html' % (schema,),
                'comments/%s/%s/insert_comments.html' % (ctype.app_label, ctype.model,),
                'comments/%s/insert_comments.html' % (ctype.model,),
                'comments/insert_comments.html',
            ),
            dict(
                schema = schema,
                object = object,
                form   = plugin.get_form(request)(request=request,initial={'content_type': ctype.id, 'object_id':object.id  }),
            ),
            context_instance = RequestContext(request)
        )
        

# --------------------------------------------------------------------------- #

class CommentsFormActionNode(Node):
    def __init__(self, schema=None, varname=None):
        self.varname = Variable(varname) if varname else None
        self.schema  = Variable(schema)  if schema  else None

    def render(self, context):
        varname = self.varname.resolve(context) if self.varname else None
        schema  = self.schema.resolve(context)  if self.schema  else None

        form_action = reverse('comments_new')

        if varname:
            context[varname] = form_action 
            return ''

        return form_action

# --------------------------------------------------------------------------- #

class CommentsListNode(Node):
    def __init__(self, object, varname, schema=None):
        self.varname = varname#Variable(varname)
        #self.schema  = Variable(schema)
        self.object = Variable(object)

    def render(self, context):
        varname = self.varname#.resolve(context)
        schema  = 'default'#self.schema.resolve(context)
        object  = self.object.resolve(context)
        context[self.varname] = get_plugin(schema).queryset(object)
        return ''

# --------------------------------------------------------------------------- #

@register.tag
def comment_form_action(parser, token):
    """
    {% comment_form_action %}  
    {% comment_form_action as [form_action] %}
    {% comment_form_action for schema [schema] %}
    {% comment_form_action for schema [schema] as [form_action] %}
    """
    bits = token.split_contents()
    length, schema, varname = len(bits), None, None

    if length not in [1, 3, 4, 6]:
        raise TemplateSyntaxError('Wrong arguments number')

    if length > 1:
        if bits[1] not in ['as', 'for']:
            raise TemplateSyntaxError('First arg must be eigher "as" or "for"')

        if bits[1] == 'as':
#            if length < 3:
#                raise TemplateSyntaxError(
#                    'Variable for %s (after "AS") not specified' % bits[0]
#                )
            varname = bits[2]

        else:
#            if length < 4:
#                raise TemplateSyntaxError('Schema name not specified')

            if  bits[2] != 'schema':
                raise TemplateSyntaxError('After "for" must follow "schema" ')

            if length > 4:
                if bits[4] != 'as':
                    raise TemplateSyntaxError(
                        'Variable for %s (after "AS") not specified' % bits[0]
                    )

                varname = bits[5]

            schema = bits[3]

    return CommentsFormActionNode(schema=schema, varname=varname)

# --------------------------------------------------------------------------- #

@register.tag
def get_comments(parser, token):
    """ 
    {% get_comments for [object] as [varname] %}
    """
    bits   = token.split_contents()
    length = len(bits)

    if length != 5:
        raise TemplateSyntaxError('Wrong arguments number')

    if bits[1] != 'for':
        raise TemplateSyntaxError('First argument must be a "for" keyword')

    if bits[3] != 'as':
        raise TemplateSyntaxError('After objects must be a "as" keyword')

    object  = bits[2]
    varname = bits[4]

    return CommentsListNode(object=object, varname=varname)

# --------------------------------------------------------------------------- #

@register.tag
def insert_comments(parser, token):
    """ 
    {% insert_comments for [object] %}
    {% insert_comments for [object] with schema [schema] %}
    """
    bits   = token.split_contents()
    length = len(bits)

    if length not in [3, 6]:
        raise TemplateSyntaxError('Wrong arguments number')

    if bits[1] != 'for':
        raise TemplateSyntaxError('First argument must be a "for" keyword')

    object = bits[2]

    if length == 6:
        if bits[3] != 'with' or bits[4] != 'schema':
            raise TemplateSyntaxError(
                'Please specify schema name after object name'
            )

        schema = bits[5]

    else:
        schema = None

    return InsertCommentsNode(object=object, schema=schema)
