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


from datetime import datetime
import os.path

import peewee

from procyon import settings as procyon_settings


__all__ = (
    'Package',
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


class Formula(object):
    name = None
    info = None
    version = None

    def check_items(self):
        if self.name and self.info and self.version:
            return True

        return False

    def install(self):
        raise NotImplementedError
