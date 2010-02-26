# -*- coding: utf-8 -*-

from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType

class CommentsQuerySet(QuerySet):
    def approved(self):
        return self.filter(is_approved=True)

    def get_for_object(self, object):
        return self.select_related().filter(
            content_type = ContentType.objects.get_for_model(object),
            object_pk    = object.pk,
        )

