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


from procyon.repo.models import Repo
from procyon.pkg.logic import get_available_packages, get_installed_packages
from procyon.pkg.logic import get_available_packages_by_name


__all__ = (
    'help',
    'freeze',
    'cache',
    'outdated',
    'search',
    'update',
    'install',
    'uninstall',
    'upgrade',
)


def help():
    """ Show available commands.
    """
    pass


def freeze():
    """ Output all currently installed packages (exact versions).
    """
    return get_installed_packages()


def cache():
    """ Output all available to install packages.
    """
    return get_available_packages()


def outdated():
    """ Output all outdated packages.
    """
    pass


def search(package):
    """ Search packages.
    """
    return get_available_packages_by_name(name=package)


def update():
    """ Update packages index.
    """
    Repo().update()


def install(packages=[]):
    """ Install packages.
    """
    pass


def uninstall(packages=[]):
    """ Uninstall packages.
    """
    pass


def upgrade(packages=[]):
    """ Upgrade packages.
    """
    pass
