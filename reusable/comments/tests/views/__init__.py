from django.http import HttpResponse
from django.template import Template, Context, add_to_builtins, TemplateSyntaxError
from reusable.comments.tests.models import ContentObject

add_to_builtins('django.templatetags.i18n')
add_to_builtins('reusable.comments.templatetags.comments_tags')

# --------------------------------------------------------------------------- #

def render(template, context):
    return Template(template).render(Context(context))

def insert_comments_brief(request):
    """
    View for testing {% insert_comments %} tag with request object in
    template context
    
    """
    return HttpResponse(
        render('{% insert_comments for object %}', dict(
                object  = ContentObject.objects.create(title='Title'),
                request = request
            )
        )
    )

def insert_comments_full(request):
    """
    View for testing {% insert_comments %} tag with request object in
    template context
    
    """
    return HttpResponse(
        render('{% insert_comments for object with schema schema %}', dict(
                object  = ContentObject.objects.create(title='Title'),
                request = request,
                schema  = 'default',
            )
        )
    )

# --------------------------------------------------------------------------- #
    
from .new import *
from .reply import  *
