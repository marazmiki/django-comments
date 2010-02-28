# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
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

USERNAME = 'john'
PASSWORD = 'qwerty123456'
EMAIL = 'john@doe.com'

def create_user(username=USERNAME, password=PASSWORD, email=EMAIL):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(
            username  = username,
            password = password,
            email    = email,
        )

    return user

from comments.tests.environment import *
from comments.tests.views import *
from comments.tests.templatetags import *
from comments.tests.managers import *
from comments.tests.forms import *
from comments.tests.settings import *
from comments.tests.last_readed import *
from comments.tests.utils import *
