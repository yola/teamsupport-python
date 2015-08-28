#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as changelog_file:
    changelog = changelog_file.read().replace('# Changelog', '')

requirements = [
    'demands',
    'lxml',
]

test_requirements = [
    'mock',
    'property-caching',
    'querylist',
]

setup(
    name='teamsupport',
    version='0.1.0',
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
        'Development Status:: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
