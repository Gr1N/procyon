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


import os.path

from git.cmd import Git
from git.exc import InvalidGitRepositoryError
from git.repo.base import Repo as GitRepo

from procyon.utils.decorators import singleton

from procyon import settings as procyon_settings


__all__ = (
    'Repo',
)


@singleton
class Repo(object):
    repo = None

    def __init__(self, *args, **kwargs):
        if not os.path.exists(procyon_settings.PROCYON_PATH):
            os.makedirs(procyon_settings.REPO_PATH)

        # TODO: make this better (exceptions, code)
        try:
            self.repo = GitRepo(path=procyon_settings.REPO_PATH)
        except InvalidGitRepositoryError:
            Git(procyon_settings.PROCYON_PATH).clone(procyon_settings.REMOTE_REPO)
            self.repo = GitRepo(path=procyon_settings.REPO_PATH)

    def update(self):
        # TODO: return True if update successful else False
        origin = self.repo.remotes.origin
        origin.pull()
