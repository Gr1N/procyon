#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import json
from tempfile import NamedTemporaryFile
import unittest

from mock import patch
import peewee

from procyon.pkg.logic import get_installed_packages, get_available_packages
from procyon.pkg.logic import get_package_data_from_json


__all__ = (
    'LogicTests',
)


fake_database = peewee.SqliteDatabase('')
fake_database.connect()


class FakePackage(peewee.Model):
    name = peewee.CharField(unique=True)
    formula_name = peewee.CharField(unique=True)
    version = peewee.CharField()
    updated_at = peewee.DateTimeField(default=datetime.now())

    class Meta:
        database = fake_database


FakePackage.create_table()


FAKE_NAME1 = 'FAKE1'
FAKE_NAME2 = 'FAKE2'
FakePackage.create(name=FAKE_NAME1, formula_name=FAKE_NAME1, version='1')
FakePackage.create(name=FAKE_NAME2, formula_name=FAKE_NAME2, version='1')


class LogicTests(unittest.TestCase):
    # TODO: clone repo with formulas or create them
    # NOTE: now for launch tests you should copy some formulas to users _procyon_ directory
    @patch('procyon.pkg.logic.Package', new=FakePackage)
    def test_installed_packages_type(self):
        packages = get_installed_packages()

        self.assertEqual(type(packages), type({}))

    @patch('procyon.pkg.logic.Package', new=FakePackage)
    def test_installed_packages_count(self):
        expected_count = FakePackage.select().count()
        packages = get_installed_packages()

        self.assertEqual(expected_count, len(packages))

    @patch('procyon.pkg.logic.Package', new=FakePackage)
    def test_installed_packages_keys(self):
        packages = get_installed_packages()

        self.assertTrue(FAKE_NAME1 in packages)
        self.assertTrue(FAKE_NAME2 in packages)

    @patch('procyon.pkg.logic.Package', new=FakePackage)
    def test_installed_packages_values(self):
        packages = get_installed_packages()

        package = packages.get(FAKE_NAME1)
        self.assertTrue('formula_name' in package)
        self.assertTrue('version' in package)
        self.assertTrue('updated_at' in package)

    def create_temporary_file(self, file_content):
        tf = NamedTemporaryFile(delete=False)
        tf.write(file_content)
        tf.close()

        return tf.name

    def test_get_package_data_from_invalid_file(self):
        tf_name = self.create_temporary_file('invalid_file')

        package_data = get_package_data_from_json(tf_name)
        self.assertEqual(package_data, (None, None))

    def test_get_package_data_from_invalid_json(self):
        tf_name = self.create_temporary_file(json.dumps('].asd'))

        package_data = get_package_data_from_json(tf_name)
        self.assertEqual(package_data, (None, None))

    def get_json_data(self, name):
        return {
            'name': name,
            'info': 'test_info1',
            'version': 1,
        }

    def test_get_package_data_from_valid_json(self):
        json_data = self.get_json_data(FAKE_NAME1)
        tf_name = self.create_temporary_file(json.dumps(json_data))

        package_data = (get_package_data_from_json(tf_name))

        self.assertEqual(type(package_data), type(()))
        name, data = package_data
        self.assertEqual(type(data), type({}))
        self.assertEqual(name, FAKE_NAME1)
        self.assertTrue('info' in data)
        self.assertTrue('formula_name' in data)
        self.assertTrue('version' in data)
        self.assertEqual(data.get('formula_name'), tf_name)

    @patch('procyon.pkg.logic.os.listdir', new=lambda ls: [])
    def test_available_packages_type(self):
        packages = get_available_packages()

        self.assertEqual(type(packages), type({}))

    def test_available_packages_valid_files(self):
        filenames = []

        def append_filename(name):
            json_data = self.get_json_data(name)
            tf_name = self.create_temporary_file(json.dumps(json_data))
            filenames.append(tf_name)

        append_filename(FAKE_NAME1)
        append_filename(FAKE_NAME2)

        with patch('procyon.pkg.logic.os.listdir', new=lambda ls: filenames):
            packages = get_available_packages()

        self.assertEqual(len(packages), 2)
        self.assertTrue(FAKE_NAME1 in packages)
        self.assertTrue(FAKE_NAME2 in packages)

    def test_available_packages_invalid_files(self):
        tf_name = self.create_temporary_file('invalid_file')

        with patch('procyon.pkg.logic.os.listdir', new=lambda ls: [tf_name]):
            packages = get_available_packages()

        self.assertFalse(packages)


if __name__ == '__main__':
    unittest.main()
