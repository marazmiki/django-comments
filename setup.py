#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Based on django setup script

import os
import sys
from distutils.core import setup
from distutils.command.install_data import install_data
from distutils.command.install import INSTALL_SCHEMES

# --------------------------------------------------------------------------- #

class osx_install_data(install_data):
    def finalize_options(self):
        self.set_undefined_options('install',
            ('install_lib', 'install_dir')
        )

        install_data.finalize_options(self)

# --------------------------------------------------------------------------- #

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []

    head, tail = os.path.split(path)

    if head == '':
        return [tail] + result

    if head == path:
        return result

    return fullsplit(head, [tail] + result)

# --------------------------------------------------------------------------- #

cmdclasses = {
    'install_data': osx_install_data if sys.platform == 'darwin' else install_data
}

# --------------------------------------------------------------------------- #


# Tell distutils to put the data_files in platform-specific installation
# locations. See here for an explanation:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)

if root_dir != '':
    os.chdir(root_dir)

django_dir = 'reusable'

for dirpath, dirnames, filenames in os.walk(django_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])
# Small hack for working with bdist_wininst.
# See http://mail.python.org/pipermail/distutils-sig/2004-August/004134.html
if len(sys.argv) > 1 and sys.argv[1] == 'bdist_wininst':
    for file_info in data_files:
        file_info[0] = '\\PURELIB\\%s' % file_info[0]

# --------------------------------------------------------------------------- #

setup(
    name         = 'django-comments',
    version      = '0.3.3a',
    description  = 'Reusable django application for threading comments based on django-mptt',
    author       = 'marazmiki',
    author_email = 'marazmiki@gmail.com',
    license      = 'BSD',
    url          = 'http://bitbucket.org/marazmiki/django-comments',
    requires     = ['django (>=1.2.3)', 'django_mptt (>0.3,<0.4)'],
    #download_url = 'http://media.djangoproject.com/releases/1.2/Django-1.2.1.tar.gz',
    packages = packages,
    cmdclass = cmdclasses,
    data_files  = data_files,
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