from django.contrib.contenttypes.models import ContentType
from comments.models import Comment

def get_commentable_object():
    return ContentType.objects.get(pk=1)

def create_comment():
    return Comment.objects.create(
        content_object = get_commentable_object(),
        content        = 'Just a test comment',
        remote_addr    = '127.0.0.1',
    )

from comments.tests.view import *
from comments.tests.template import *
