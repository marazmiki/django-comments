# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name         = 'django-comments',
    version      = '0.1a',
    description  = 'Reusable django application for threading comments based on django-mptt',
    author       = 'marazmiki',
    author_email = 'marazmiki@gmail.com',
    license      = 'BSD',
    url          = 'http://bitbucket.org/marazmiki/django-comments',
    requires     = ['django', 'mptt'],
    packages     = [
        'comments',
        'comments.templatetags',
        'comments.tests',
        'comments.tests',
        'comments_plugins',
        'comments_plugins.guest',
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Message Boards',
        'Topic :: Utilities',
    ]
)

