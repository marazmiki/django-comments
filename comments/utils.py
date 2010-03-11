# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType
from comments.models import CommentSettings, Comment, LastReadedComment

def get_settings_for_object(object):
    try:
        return CommentSettings.objects.get_for_object(object)[0]
    except (IndexError, CommentSettings.DoesNotExist):
        return CommentSettings()

def count_comments_for_object(content_object):
    return Comment.objects.get_for_object(content_object).approved().count()

def update_last_readed_comment(user, content_object):
    last = Comment.objects.get_for_object(content_object).order_by('-id')

    if len(last):
        last_comment = last[0]

        readed, created = LastReadedComment.objects.get_or_create(
            user         = user,
            object_pk    = content_object.pk,
            content_type = ContentType.objects.get_for_model(content_object),
            defaults     = dict(comment=last_comment)
        )

        if not created and readed.comment != last_comment:
            readed.comment = last_comment
            readed.save()

        return readed.comment

def count_unreaded_comments(object, user):
    last = LastReadedComment.objects.get_for_user_and_object(user, object)

    return Comment.objects.get_for_object(object).              \
        filter(pk__gt=last.comment.pk).count() if last else     \
        count_comments_for_object(object)
    
    
