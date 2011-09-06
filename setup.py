#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import os

version='0.5'
package = 'comments'

setup(
    name = 'django-comments',
    version = version,
    author  = 'marazmiki',
    author_email = 'marazmiki@gmail.com',
    url = 'http://pypi.python.org/pypi/django-comments',
    download_url = 'http://bitbucket.org/marazmiki/django-comments/get/tip.zip',
    description = 'Generic pluggable comments application',
    long_description = open('README.rst').read(),
    license = 'MIT license',
    requires = ['django (>=1.3)'],
    packages=['comments'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
