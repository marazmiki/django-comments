# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.contenttypes.models import ContentType
from comments.query import CommentsQuerySet, LastReadedCommentQuerySet

class BaseManager(models.Manager):
    def get_query_set(self):
        return CommentsQuerySet(self.model)

    def get_for_object(self, object):
        return self.get_query_set().select_related().\
            filter(
                content_type = ContentType.objects.get_for_model(object),
                object_pk    = object.pk,
            )

class CommentManager(BaseManager):
    def approved(self):
        return self.get_query_set().filter(is_approved=True)

class CommentSettingsManager(BaseManager):
    pass

class LastReadedCommentManager(BaseManager):
    def get_query_set(self):
        return LastReadedCommentQuerySet(self.model)
        
    def get_for_user_and_object(self, user, content_object):
        lasts = self.get_for_object(content_object).filter(user=user)[:1]
        return lasts[0] if lasts else None
