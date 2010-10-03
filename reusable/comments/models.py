# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from reusable.comments.managers import GenericObjectManager
import mptt

# --------------------------------------------------------------------------- #

class GenericObject(models.Model):
    """
    Базовая модель, обеспечивающая функциональность generic relation
    """
    object_id      = models.CharField(max_length=255)
    content_type   = models.ForeignKey(ContentType)
    content_object = generic.GenericForeignKey(
        ct_field   = 'content_type',
        fk_field   = 'object_id',
    )

    objects = GenericObjectManager()

    class Meta:
        abstract = True

# --------------------------------------------------------------------------- #

# Leave compatible with django-mptt 0.3
class MetaClass:
    abstract = True
try:
    from mptt.models import MPTTModel
    class Signature(MPTTModel, GenericObject): pass
except ImportError, e:
    class Signature(GenericObject, models.Model): pass 

#if hasattr(__import__(mptt.models), 'MPTTModel'):
#    class Signature(mptt.models.MPTTModel, GenericObject): pass
#else:
#    class Signature(GenericObject, models.Model): pass 

Signature.Meta = MetaClass    

# --------------------------------------------------------------------------- #

class AbstractComment(Signature):
    """
    Базовая модель комментария
    """
    #parent_comment = models.ForeignKey('self', related_name='replies', null=True, blank=True)
    parent = models.ForeignKey('self', related_name='replies', null=True, blank=True)
    date_created   = models.DateTimeField(default=datetime.now, editable=False)
    content        = models.TextField(default='')
    remote_addr    = models.IPAddressField(blank=True, null=True)
    forwarded_for  = models.IPAddressField(blank=True, null=True)

    def has_replies(self):
        return self.rght - self.lft > 1

    def parent_id(self):
        return self.__dict__['parent_comment_id']

    def __unicode__(self):
        return self.content

    class Meta:
        abstract = True
        app_label = 'comments'
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    class MPTTMeta:
        order_insertion_by = ['date_created']
        #parent_attr = 'parent_comment'
        
# --------------------------------------------------------------------------- #

if hasattr(mptt, 'register'):
    # django-mptt < 0.4
    # This line looks frightening, suggestions for alternatives welcome :)   
    mptt.register(AbstractComment, 
        **dict([
            (attr, getattr(AbstractComment.MPTTMeta, attr)) for attr in dir(AbstractComment.MPTTMeta) if attr[:1] != '_']
        )
    )
