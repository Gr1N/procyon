#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='Procyon',
    version='0.0.1',
    description='Package manager for OSTIS',
    author='Nikita Grishko',
    author_email='grin.minsk@gmail.com',
    install_requires=[
        'GitPython>=0.3.2.RC1',
        'peewee>=1.0.0',
    ],
    classifiers=[
        'Development Status :: Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
    ],
    url='https://github.com/Gr1N/procyon/',
    packages=[
        'procyon',
        'procyon.pkg',
        'procyon.repo',
    ],
)
