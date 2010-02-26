# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name         = 'Distutils',
    version      = '1.0',
    description  = 'Python Distribution Utilities',
    author       = 'Greg Ward',
    author_email = 'gward@python.net',
    url          = 'http://www.python.org/sigs/distutils-sig/',
    packages     = ['comments', 'comments.admin', 'comments.templatetags', 'comments.tests',
    ],
)

