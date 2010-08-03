# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.contenttypes.models import ContentType
from comments.query import GenericObjectQuerySet

# --------------------------------------------------------------------------- #

class GenericObjectManager(models.Manager):
    def get_query_set(self):
        return GenericObjectQuerySet(self.model)

    def get_for_object(self, object):
        return self.get_query_set().filter(
            content_type = ContentType.objects.get_for_model(object),
            object_id    = object.pk,
        )