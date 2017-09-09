#!/usr/bin/env python

from distutils.core import setup

__author__ = 'Martin Ertsås'
__author_email__ = 'martiert@gmail.com',
__copyright__ = 'Copyright (c) 2017 Martin Ertsås'
__license__ = 'MIT'

setup(
    name='aiosparkapi',

    version='0.1',

    description='Asyncio library for cisco spark api',

    author='Martin Ertsås',
    author_email='martiert@gmail.com',

    url='https://github.com/martiert/aiosparkapi',

    license=__license__ + ';' + __copyright__,

    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Education',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='cisco spark api async enterprise messaging',

    packages=['aiosparkapi'],
    install_requires=['aiohttp>=2.2.5'],
)
