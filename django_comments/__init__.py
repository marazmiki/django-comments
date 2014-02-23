# coding: utf-8

from __future__ import unicode_literals

VERSION = (2, 0, 0, 'b')


def get_version():
    return '.'.join(map(unicode, VERSION))


__author__ = 'Mikhail Porokhovnichenko'
__version__ = get_version()
