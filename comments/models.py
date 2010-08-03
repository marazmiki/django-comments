# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from mptt import register, registry
from comments.managers import GenericObjectManager

# --------------------------------------------------------------------------- #

class GenericObject(models.Model):
    """
    Базовая модель, обеспечивающая функциональность generic relation
    """
    object_id      = models.TextField()
    content_type   = models.ForeignKey(ContentType)
    content_object = generic.GenericForeignKey(
        ct_field   = 'content_type',
        fk_field   = 'object_id',
    )

    objects = GenericObjectManager()

    class Meta:
        abstract = True

# --------------------------------------------------------------------------- #

class AbstractComment(GenericObject):
    """
    Базовая модель комментария
    """
    parent_comment = models.ForeignKey('self', related_name='childs', null=True, blank=True)
    date_created   = models.DateTimeField(default=datetime.now, editable=False)
    content        = models.TextField(default='')
    remote_addr    = models.IPAddressField(blank=True, null=True)
    forwarded_for  = models.IPAddressField(blank=True, null=True)

    def has_replies(self):
        return self.rght - self.lft > 1

    def __unicode__(self):
        return self.content

    class Meta:
        app_label = 'comments'
        verbose_name = _('comment')
        verbose_name_plural = _('comments')


    class Meta:
        abstract = True

# --------------------------------------------------------------------------- #

if AbstractComment not in registry:
    register(AbstractComment,
        parent_attr = 'parent_comment',
        order_insertion_by = ['date_created', ],
    )
    
