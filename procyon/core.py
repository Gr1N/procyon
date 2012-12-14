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

from procyon.repo.logic import update_repo
from procyon.pkg.logic import get_available_packages, get_installed_packages
from procyon.pkg.logic import get_available_packages_by_name, get_outdated_packages
from procyon.pkg.logic import install_package, uninstall_package


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
    """Show available commands.
    """
    pass


def freeze():
    """Output all currently installed packages (exact versions).
    """
    return get_installed_packages()


def cache():
    """Output all available to install packages.
    """
    return get_available_packages()


def outdated():
    """Output all outdated packages.
    """
    return get_outdated_packages()


def search(package):
    """Search packages.
    """
    return get_available_packages_by_name(name=package)


def update():
    """Update packages index.
    """
    return update_repo()


def install(packages=[]):
    """Install packages.
    """
    installed = []
    for package in packages:
        installed.append((package, install_package(package)))
    return installed


def uninstall(packages=[]):
    """Uninstall packages.
    """
    uninstalled = []
    for package in packages:
        uninstalled.append((package, uninstall_package(package)))
    return uninstalled


def upgrade(packages=[]):
    """Upgrade package.
    """
    uninstalled = uninstall(packages)
    installed = []
    if not uninstalled:
        installed = install(uninstalled)
    return installed
