from django.contrib.contenttypes.models import ContentType
from comments.models import Comment

def get_content_object(pk=1):
    return ContentType.objects.get(pk=pk)

def create_comment(object_id=1):
    return Comment.objects.create(
        content_object = get_content_object(object_id),
        content        = 'Just a test comment',
        remote_addr    = '127.0.0.1',
    )

from comments.tests.view import *
from comments.tests.template import *
from comments.tests.manager import *
from comments.tests.form import *