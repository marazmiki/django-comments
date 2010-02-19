from django.contrib.contenttypes.models import ContentType

def get_commentable_object():
    return ContentType.objects.get(pk=1)

from comments.tests.view import *
from comments.tests.template import *
