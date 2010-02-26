# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.contenttypes.models import ContentType
from comments.query import CommentsQuerySet

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
