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

from datetime import datetime
import hashlib
import os
import shutil
import tarfile
from urllib import urlretrieve
from urlparse import urlparse
import zipfile

import peewee

from procyon import settings as procyon_settings


__all__ = (
    'Package',
    'InstallationStatuses',
    'Formula',
)


database = os.path.join(procyon_settings.PROCYON_PATH, procyon_settings.PACKAGES_DB_NAME)
database = peewee.SqliteDatabase(database)
database.connect()


class Package(peewee.Model):
    name = peewee.CharField(db_index=True, unique=True)
    formula_name = peewee.CharField(db_index=True, unique=True)
    version = peewee.CharField()
    updated_at = peewee.DateTimeField(default=datetime.now())

    class Meta:
        database = database


if not Package.table_exists():
    Package.create_table()


class InstallationStatuses:
    FORMULA_NOT_FOUND = 0
    BAD_FORMULA = 1
    BAD_URL = 2
    DOWNLOAD_ERROR = 3
    BAD_FILE_TYPE = 4
    MD5SUM_CHECK_ERROR = 5
    DOWNLOAD_OK = 6
    EXTRACT_ERROR = 7
    EXTRACT_OK = 8
    INSTALL_OK = 9
    INSTALL_ERROR = 10
    ALREADY_INSTALLED = 11
    NOT_INSTALLED = 12
    UNINSTALL_OK = 13
    UNINSTALL_ERROR = 14


class Formula(object):
    name = None
    info = None
    version = None
    homepage = None

    url = None
    md5sum = None

    def check_items(self):
        if self.name and self.info and self.version and self.url:
            return True

        return False

    def _check_md5sub(self, tmp_file):
        md5 = hashlib.md5()

        with open(tmp_file, 'rb') as f:
            for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
                md5.update(chunk)

        return md5.hexdigest() == self.md5sum

    def _download(self):
        allowed_schemes = [
            'http',
            'https',
        ]
        scheme = urlparse(self.url).scheme
        if scheme not in allowed_schemes:
            return InstallationStatuses.BAD_URL, None

        try:
            tmp_file, info = urlretrieve(self.url)
        except IOError:
            return InstallationStatuses.DOWNLOAD_ERROR, None

        if not zipfile.is_zipfile(tmp_file) and not tarfile.is_tarfile(tmp_file):
            return InstallationStatuses.BAD_FILE_TYPE, None

        if self.md5sum and not self._check_md5sub(tmp_file):
            return InstallationStatuses.MD5SUM_CHECK_ERROR, None

        return InstallationStatuses.DOWNLOAD_OK, tmp_file

    def _extract(self, tmp_file):
        if zipfile.is_zipfile(tmp_file):
            arc = zipfile.ZipFile(tmp_file)
        elif tarfile.is_tarfile(tmp_file):
            arc = tarfile.TarFile(tmp_file)
        else:
            return InstallationStatuses.BAD_FILE_TYPE

        install_dir = os.path.join(procyon_settings.INSTALL_PATH, self.name)
        if not os.path.exists(install_dir):
            os.makedirs(install_dir)

        try:
            arc.extractall(path=install_dir)
        except (zipfile.BadZipfile, zipfile.LargeZipFile, tarfile.ReadError, tarfile.ExtractError):
            return InstallationStatuses.EXTRACT_ERROR

        return InstallationStatuses.EXTRACT_OK

    def install(self):
        if not self.check_items():
            return InstallationStatuses.BAD_FORMULA

        status, tmp_file = self._download()
        if status != InstallationStatuses.DOWNLOAD_OK:
            return status

        # TODO: install dependencies

        status = self._extract(tmp_file)
        if status != InstallationStatuses.EXTRACT_OK:
            return status

        return InstallationStatuses.INSTALL_OK

    def uninstall(self):
        if not self.check_items():
            return InstallationStatuses.BAD_FORMULA

        install_dir = os.path.join(procyon_settings.INSTALL_PATH, self.name)
        if not os.path.exists(install_dir):
            return InstallationStatuses.NOT_INSTALLED

        shutil.rmtree(install_dir)

        # TODO: uninstall dependencies

        return InstallationStatuses.UNINSTALL_OK
