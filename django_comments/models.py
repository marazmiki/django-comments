# coding: utf-8

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django_comments.plugins import plugin_pool
from django_comments.settings import PLUGINS, SYSTEM_DEFAULT_PLUGIN
from generic_helpers.models import GenericRelationModel


def default_plugin_enabled():
    return SYSTEM_DEFAULT_PLUGIN in PLUGINS


class DateCreatedMixin(models.Model):
    """
    Abstract model with a `date_created` field
    """
    date_created = models.DateTimeField(_('created at'), editable=False,
                                        db_index=True, default=now)

    class Meta(object):
        abstract = True


class Comment(DateCreatedMixin, GenericRelationModel):
    """
    Default comment model
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments',
                             verbose_name=_('user'),
                             blank=True, null=True)
    author_name = models.CharField(_('author name'), max_length=255,
                                   default='')
    content = models.TextField(_('text'), default='', blank=False)

    class Meta(object):
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        managed = default_plugin_enabled()
        ordering = ['-date_created']
        index_together = [('content_type', 'object_pk')]


for plugin in PLUGINS:
    plugin_pool.register(plugin)
