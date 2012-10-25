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

from procyon.pkg.models import Package
from procyon.repo.decorators import repo_required

from procyon import settings as procyon_settings


__all__ = (
    'get_available_packages',
    'get_available_packages_by_name',
    'get_installed_packages',
)


def get_available_packages():
    u"""Returns dictionary with available to install packages from repo.
    """
    formulas_dir = os.path.join(
        procyon_settings.REPO_PATH, procyon_settings.FORMULAS_DIR_NAME
    )
    packages = {}

    for modulename in os.listdir(formulas_dir):
        if modulename != '__init__.py' and not modulename.endswith('.pyc'):
            package_name, package_data = get_package_data(modulename)

            if package_name and package_data:
                packages.setdefault(package_name, package_data)

    return packages


def get_available_packages_by_name(name):
    u"""Returns dictionary with available to install packages from repo with
    specified package name.
    """
    def prepare_name(name):
        name = str(name).lower()

        for to_replace in ['-', '_', '/', ' ', '[', ']']:
            name = name.replace(to_replace, '')

        return name

    name = prepare_name(name)
    packages = {}

    for package_name, package_data in get_available_packages().iteritems():
        prepared_pkg_name = prepare_name(package_name)

        if name in prepared_pkg_name or prepared_pkg_name in name:
            packages.setdefault(package_name, package_data)

    return packages


def get_installed_packages():
    u"""Returns dictionary with all installed packages.
    """
    packages = {}

    for entry in Package.select():
        packages.setdefault(entry.name, {
            'formula_name': entry.formula_name,
            'version': entry.version,
            'updated_at': entry.updated_at,
        })

    return packages


def import_formula_module(modulename):
    absolute_modulename = modulename.split('.')[0]
    try:
        formula = __import__(absolute_modulename).Formula
        return formula if formula.check_items else None
    except AttributeError:
        return None


def get_package_data(modulename):
    u"""Returns parsed information about package from *.json file with
    passed file name via arguments.
    """
    formula = import_formula_module(modulename)

    if not formula:
        return None, None

    name = formula.name
    data = {
        'info': formula.info,
        'formula_name': modulename,
        'version': formula.version,
    }

    return name, data
