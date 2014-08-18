# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


VERSION = (2, 0, 0, 'b')


def get_version():
    return '.'.join(map(unicode, VERSION))


__author__ = 'Mikhail Porokhovnichenko'
__version__ = get_version()


default_app_config = 'django_comments.apps.CommentsConfig'