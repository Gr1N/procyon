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

import os.path

from procyon import settings as procyon_settings
from procyon.pkg.models import Package, InstallationStatuses


__all__ = (
    'get_available_packages',
    'get_available_packages_by_name',
    'get_installed_packages',
    'get_outdated_packages',
    'install_package',
    'uninstall_package',
    'upgrade_package',
)


def get_available_packages():
    """Returns dictionary with available to install packages from repo.
    """
    available = {}

    for modulename in os.listdir(procyon_settings.REPO_PATH):
        if modulename != '__init__.py' and modulename.endswith('.py'):
            package_name, package_data = get_package_data(modulename)

            if package_name and package_data:
                available.setdefault(package_name, package_data)

    return available


def get_available_packages_by_name(name):
    """Returns dictionary with available to install packages from repo with
    specified package name.
    """
    def prepare_name(name):
        name = str(name).lower()

        for to_replace in ['-', '_', '/', ' ', '[', ']']:
            name = name.replace(to_replace, '')

        return name

    name = prepare_name(name)
    available = {}

    for package_name, package_data in get_available_packages().iteritems():
        prepared_pkg_name = prepare_name(package_name)

        if name in prepared_pkg_name or prepared_pkg_name in name:
            available.setdefault(package_name, package_data)

    return available


def get_installed_packages():
    """Returns dictionary with all installed packages.
    """
    installed = {}

    for entry in Package.select():
        installed.setdefault(entry.name, {
            'formula_name': entry.formula_name,
            'version': entry.version,
            'updated_at': entry.updated_at,
        })

    return installed


def check_version(available_version, installed_version):
    available_lpart, dot, available_rpart = available_version.partition('.')
    installed_lpart, dot, installed_rpart = installed_version.partition('.')

    if int(available_lpart) > int(installed_lpart):
        return True
    elif int(available_lpart) < int(installed_lpart):
        return False
    elif len(available_rpart) == 0:
        return False
    elif len(available_rpart) != 0 and len(installed_rpart) == 0:
        return True
    else:
        return check_version(available_rpart, installed_rpart)


def get_outdated_packages():
    """Returns dictionary with outdated installed packages.
    """
    installed = get_installed_packages()
    available = get_available_packages()

    outdated = {}

    for package_name, package_data in installed.iteritems():
        available_version = available.get(package_name, {}).get('version', None)
        installed_version = package_data.get('version')

        if available_version and check_version(available_version, installed_version):
            package_data.update({
                'available_version': available_version,
            })
            outdated.setdefault(package_name, package_data)

    return outdated


def import_formula_module(modulename):
    absolute_modulename = modulename.split('.')[0]
    try:
        formula = __import__(absolute_modulename).Formula()
        return formula if formula.check_items() else None
    except (AttributeError, ImportError):
        return None


def get_package_data(modulename):
    """Returns parsed information about package from *.json file with
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


def install_package(name):
    available = get_available_packages()
    if name not in available:
        return InstallationStatuses.FORMULA_NOT_FOUND

    packages = [package.name for package in Package.select().where(Package.name == name)]
    if len(packages) > 1:
        return InstallationStatuses.INSTALL_ERROR
    elif packages and packages[0] == name:
        return InstallationStatuses.ALREADY_INSTALLED

    package = available.get(name)
    formula = import_formula_module(package.get('formula_name'))
    if not formula:
        return InstallationStatuses.BAD_FORMULA

    status = formula.install()
    if status != InstallationStatuses.INSTALL_OK:
        return status

    Package.create(
        name=formula.name,
        formula_name=package.get('formula_name'),
        version=formula.version
    )

    return status


def uninstall_package(name):
    installed = get_installed_packages()
    if name not in installed:
        return InstallationStatuses.NOT_INSTALLED

    package = installed.get(name)
    formula = import_formula_module(package.get('formula_name'))
    if not formula:
        return InstallationStatuses.BAD_FORMULA

    status = formula.uninstall()
    if status != InstallationStatuses.UNINSTALL_OK:
        return status

    package = Package.get(name=name)
    package.delete_instance()

    return status


def upgrade_package(name):
    raise NotImplementedError
