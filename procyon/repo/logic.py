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

from git.cmd import Git
from git.exc import InvalidGitRepositoryError, GitCommandError, NoSuchPathError
from git.repo.base import Repo as GitRepo

from procyon import settings as procyon_settings


__all__ = (
    'update_repo',
)


def open_or_clone_repo():
    """Returns opened or cloned repo and 'True' flag if operation successful
    else 'None' object and 'False' flag.
    """
    try:
        return GitRepo(path=procyon_settings.REPO_PATH), True
    except (InvalidGitRepositoryError, NoSuchPathError):
        pass

    try:
        Git(procyon_settings.PROCYON_PATH).clone(procyon_settings.REMOTE_REPO)
    except GitCommandError:
        return None, False

    return GitRepo(path=procyon_settings.REPO_PATH), True


def update_repo():
    """Returns 'True' and hexshas if operation successful else 'False' and
    none-hexshas. If raises some erros when repo updating, return 'False',
    current repo hash and none-hexsha.
    """
    repo, successful = open_or_clone_repo()

    if not successful:
        return False, None, None

    hexsha = lambda r: r.heads.master.commit.tree.hexsha
    before_up_hexhsha = hexsha(repo)

    try:
        origin = repo.remotes.origin
        origin.pull()
    except GitCommandError:
        return False, before_up_hexhsha, None
    except AssertionError:
        pass

    after_up_hexsha = hexsha(repo)
    return True, before_up_hexhsha, after_up_hexsha
