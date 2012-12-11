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

import message

from procyon.pkg.models import InstallationStatuses


__all__ = (
    'get_installation_status',
    'get_uninstallation_status',
    'get_update_status',
    'get_repo_setting_status',
    'get_package_list_info',
)


installation_statuses = {
    InstallationStatuses.INSTALL_OK: 'Package %s succesfully installed',
    InstallationStatuses.FORMULA_NOT_FOUND: 'Selected package %s was not found',
    InstallationStatuses.ALREADY_INSTALLED: 'Selected package %s is already installed',
    InstallationStatuses.BAD_FORMULA: 'Error occured during %s formula processing',
    InstallationStatuses.BAD_URL: 'Transfer error occured during %s package installation. Only http/https allowed',
    InstallationStatuses.DOWNLOAD_ERROR: 'Transfer error occured during %s package installation',
    InstallationStatuses.BAD_FILE_TYPE: 'Transfer error occured during %s package installation. Only zip/tar archieves allowed',
    InstallationStatuses.EXTRACT_ERROR: 'Error occured during %s package exctraction',
    InstallationStatuses.UNINSTALL_OK:'Package %s succesfully removed',
    InstallationStatuses.NOT_INSTALLED: 'Selected package %s is not installed',
}


def get_installation_status(package):
    status = installation_statuses.get(package[1])
    if status:
        return status % package[0]
    return 'Error occured during %s package installation' % package[0]


def get_uninstallation_status(package):
    status = installation_statuses.get(package[1])
    if status:
        return status % package[0]
    return 'Error occured during %s package removing' % package[0]


def get_update_status(result):
    if result[0]:
        return 'Package list succesfully updated from %s to %s' % (str(result[1]), str(result[2]))
    else:
        return 'Update was not performed'


def get_repo_setting_status(result):
    if result[0]:
        return 'Remote repo succesfully set'
    else:
        return 'Error occured during remote repo setting. %s' % result[1]


def get_package_list_info(client_command, packages):
    command_name = 'get_%s_package_list_info' % client_command
    command = getattr(message, command_name, None)
    return command(packages)


def get_installed_package_list_info(packages):
    info = []
    info.append('Installed package list:')
    for package_name, package_info in packages.iteritems():
        info.append('\n%s v%s' % (package_info.get('formula_name'), package_info.get('version')))
        info.append('last updated at %s' % package_info.get('updated_at'))
    return info


def get_available_package_list_info(packages):
    info = []
    info.append('Available package list:')
    for package_name, package_info in packages.iteritems():
        info.append('\n%s v%s' % (package_name, package_info.get('version')))
        info.append(package_info.get('info'))
    return info


def get_outdated_package_list_info(packages):
    info = []
    info.append('Outdated package list:')
    for package_name, package_info in packages.iteritems():
        info.append('\n%s v%s' % (package_info.get('formula_name'), package_info.get('version')))
        info.append('last updated at %s' % package_info.get('updated_at'))
        info.append('available v%s' % package_info.get('available_version'))
    return info
