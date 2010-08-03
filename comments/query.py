# -*- coding: utf-8 -*-

from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType

# --------------------------------------------------------------------------- #

class GenericObjectQuerySet(QuerySet):
    def get_for_object(self, object):
        return self.select_related().filter(
            content_type = ContentType.objects.get_for_model(object),
            object_id    = object.pk,
        )