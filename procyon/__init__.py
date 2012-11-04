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


from __future__ import unicode_literals

import os
import sys
import warnings


__all__ = (
    'settings',
)


default_settings = {
    # global settings
    'PROCYON_PATH': os.path.expanduser('~/.procyon'),

    # repo settings
    'REPO_PATH': '',
    'REMOTE_REPO': '',

    # packaging settings
    'PACKAGES_DB_NAME': 'packges.db',
}


class Settings:
    def __init__(self):
        for k, v in default_settings.items():
            setattr(self, k, v)


settings = Settings()

if not settings.REMOTE_REPO:
    warnings.showwarning(
        'Missed remote repository parameter',
        UserWarning,
        'procyon/__init__.py',
        44
    )

if not os.path.exists(settings.PROCYON_PATH):
    os.makedirs(settings.PROCYON_PATH)

if not getattr(settings, 'REPO_PATH', None):
    git_name = settings.REMOTE_REPO.split('/')[-1]
    repo_name = git_name.split('.')[0]
    settings.REPO_PATH = os.path.join(settings.PROCYON_PATH, repo_name)

sys.path.append(settings.REPO_PATH)
