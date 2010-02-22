# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.contenttypes.models import ContentType

class CommentManager(models.Manager):
    def get_for_object(self, object):
        return super(CommentManager, self).get_query_set().select_related().\
            filter(
                content_type = ContentType.objects.get_for_model(object),
                object_pk    = object.pk,
            )

class CommentSettingsManager(CommentManager):
    pass