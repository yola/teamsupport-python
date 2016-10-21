#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import re

from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('teamsupport/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.rst') as changelog_file:
    changelog = changelog_file.read()

requirements = [
    'demands>=4.0.0, < 5.0.0',
    'lxml>=3.4.4',
    'property-caching>=1.0.3',
    'querylist>=0.2.0',
    'six<2.0.0',
    'python-dateutil<3.0.0',
]

test_requirements = [
    'mock<1.2.0',
    'funcsigs<0.5',
]

setup(
    name='teamsupport',
    version=version,
    description='Python library for interfacing with the TeamSupport API',
    long_description=readme + '\n\n' + changelog,
    author='Yola Engineers',
    author_email='engineers@yola.com',
    url='https://github.com/yola/teamsupport-python',
    packages=[
        'teamsupport',
    ],
    include_package_data=True,
    install_requires=requirements,
    license='MIT',
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
