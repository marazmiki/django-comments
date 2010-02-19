# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from comments.managers import CommentManager

class Comment(models.Model):
    content        = models.TextField()
    date_created   = models.DateTimeField(blank=True, default=datetime.now())
    date_changed   = models.DateTimeField(blank=True, default=datetime.now())
    is_approved    = models.BooleanField(default=True)
    content_type   = models.ForeignKey('contenttypes.ContentType')
    object_pk      = models.TextField()
    remote_addr    = models.IPAddressField(blank=True, default='')
    forwarded_for  = models.IPAddressField(blank=True, null=True)
    parent_comment = models.ForeignKey('self', blank=True, null=True)
    content_object = generic.GenericForeignKey(
        ct_field   = 'content_type',
        fk_field   = 'object_pk',
    )

    objects = CommentManager()

    def __unicode__(self):
        return self.content

    class Meta:
        app_label = 'comments'
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

