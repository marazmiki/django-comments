# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from mptt import register as mptt_register, registry as mptt_registry
from comments.settings import PREMODERATE, ENABLED, LEVEL_LIMIT
from comments.managers import CommentManager, CommentSettingsManager, LastReadedCommentManager

# --------------------------------------------------------------------------- #

class CommentBase(models.Model):
    content_type   = models.ForeignKey('contenttypes.ContentType')
    object_pk      = models.TextField()
    content_object = generic.GenericForeignKey(
        ct_field   = 'content_type',
        fk_field   = 'object_pk',
    )

    class Meta:
        app_label = 'comments'
        abstract = True

# --------------------------------------------------------------------------- #

class Comment(CommentBase):
    content        = models.TextField()
    date_created   = models.DateTimeField(blank=True, default=datetime.now)
    date_changed   = models.DateTimeField(blank=True, default=datetime.now)
    is_approved    = models.BooleanField(default=True)
    parent_comment = models.ForeignKey('self', blank=True, null=True, related_name='children')
    remote_addr    = models.IPAddressField(blank=True, default='')
    forwarded_for  = models.IPAddressField(blank=True, null=True)

    objects = CommentManager()

    def __unicode__(self):
        return self.content

    class Meta:
        app_label = 'comments'
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        permissions = (
            ('can_see_ip',          unicode(_('Can see commenting IP'))),
            ('can_delete_comment',  unicode(_('Can delete comment'))),
            ('can_edit_comment',    unicode(_('Can edit comment'))),
            ('can_approve_comment', unicode(_('Can approve and blame comments'))),
        )

# --------------------------------------------------------------------------- #

class CommentSettings(CommentBase):
    premoderate = models.BooleanField(
        default      = PREMODERATE,
        blank        = True,
        verbose_name = _('Premoderate'),
        help_text    = _('Enable premoderation for this content object')
    )

    enabled = models.BooleanField(
        default      = ENABLED,
        blank        = True,
        verbose_name = _('Enable comments'),
        help_text    = _('Enables comment for this content object')
    )

    level_limit = models.PositiveIntegerField(
        default      = LEVEL_LIMIT,
        blank        = True,
        verbose_name = _('Nest depth'),
        help_text    = _('Specify 0 if no level limit needed'))

    objects = CommentSettingsManager()

    def __unicode__(self):
        return unicode(self.content_object)

    class Meta:
        app_label = 'comments'
        verbose_name = _('Object specified settings')
        verbose_name_plural = _('Object specified settings')
        unique_together = ('content_type', 'object_pk')

# --------------------------------------------------------------------------- #

class LastReadedComment(CommentBase):
    user    = models.ForeignKey(User, related_name='last_readed_comments')
    comment = models.ForeignKey(Comment, related_name='last_readed_comments')
    objects = LastReadedCommentManager()

    def __unicode__(self):
        return unicode(self.comment)

    class Meta:
        app_label = 'comments'
        unique_together = [('user', 'content_type', 'object_pk', ), ]

# --------------------------------------------------------------------------- #

if Comment not in mptt_registry:
    mptt_register(Comment,
        parent_attr = 'parent_comment',
        order_insertion_by = ['date_created', ],
    )
