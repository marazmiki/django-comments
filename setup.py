#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from django_comments import get_version
import os

package = 'django_comments'

setup(
    name = 'django-comments',
    version = get_version(),
    author  = 'marazmiki',
    author_email = 'marazmiki@gmail.com',
    url = 'http://pypi.python.org/pypi/django-comments',
    download_url = 'https://github.com/marazmiki/django-comments/zipball/master',
    description = 'Generic pluggable comments application',
    long_description = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    license = 'MIT license',
    requires = ['django (>=1.3)'],
    packages=find_packages(),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
