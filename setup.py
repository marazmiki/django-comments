#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
from django_comments import get_version
import os


package = 'django_comments'


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as fp:
    long_description = fp.read()


tests_require = ['Django',
                 'requests',
                 'six']

setup(name='django-comments',
      version=get_version(),
      author='Mikhail Porokhovnichenko',
      author_email='marazmiki@gmail.com',
      url='https://github.com/marazmiki/django-comments',
      download_url='https://github.com/marazmiki/django-comments/zipball/master',
      description='Generic pluggable comments application',
      long_description=long_description,
      license='MIT license',
      requires=['django'],
      packages=find_packages(),
      test_suite='tests.main',
      tests_require=tests_require,
      include_package_data=True,
      classifiers=['Development Status :: 4 - Beta',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules'])
