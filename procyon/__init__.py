#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Procyon <https://github.com/Gr1N/procyon>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import os
import sys


__all__ = (
    'settings',
)


default_settings = {
    # global settings
    'PROCYON_PATH': os.path.expanduser('~/.procyon'),

    # repo settings
    'REPO_NAME': 'procyon',
    'REPO_PATH': None,
    'REMOTE_REPO': 'git://github.com/Gr1N/procyon.git',
    'FORMULAS_DIR_NAME': 'formulas',

    # packaging settings
    'PACKAGES_DB_NAME': 'packges.db',
}


class Settings:
    def __init__(self):
        for k, v in default_settings.items():
            setattr(self, k, v)


settings = Settings()

if not os.path.exists(settings.PROCYON_PATH):
    os.makedirs(settings.PROCYON_PATH)

if not getattr(settings, 'REPO_PATH', None):
    settings.REPO_PATH = os.path.join(settings.PROCYON_PATH, settings.REPO_NAME)

formulas_path = os.path.join(settings.REPO_PATH, settings.FORMULAS_DIR_NAME)
sys.path.append(formulas_path)
