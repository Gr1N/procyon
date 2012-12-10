#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime
import unittest

from mock import patch, MagicMock
import peewee

from procyon.pkg.logic import get_installed_packages, get_available_packages
from procyon.pkg.logic import get_available_packages_by_name, get_outdated_packages
from procyon.pkg.logic import check_version, install_package, uninstall_package
from procyon.pkg.models import InstallationStatuses


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


@patch('procyon.pkg.logic.Package', new=FakePackage)
class LogicTests(unittest.TestCase):
    # TODO: clone repo with formulas or create them
    # NOTE: now for launch tests you should copy some formulas to users _procyon_ directory
    def setUp(self):
        FakePackage.create(name=FAKE_NAME1, formula_name=FAKE_NAME1, version='1')
        FakePackage.create(name=FAKE_NAME2, formula_name=FAKE_NAME2, version='1')

    def tearDown(self):
        def delete_package(name):
            try:
                p = FakePackage.get(name=name)
                p.delete_instance()
            except FakePackage.DoesNotExist:
                pass

        delete_package(FAKE_NAME1)
        delete_package(FAKE_NAME2)

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

    @patch('procyon.pkg.logic.os.listdir', new=lambda ls: [])
    def test_available_packages_type(self):
        packages = get_available_packages()

        self.assertEqual(type(packages), type({}))

    def create_fake_import(self, name, version='1', check_items=True,
        install_status=InstallationStatuses.INSTALL_OK, uninstall_status=InstallationStatuses.UNINSTALL_OK):
        filenames = []
        filenames.append('%s.py' % FAKE_NAME1)

        import_mock = MagicMock()
        fake_package = MagicMock()
        fake_package.name = name
        fake_package.version = version
        fake_package.check_items.return_value = check_items
        fake_package.install.return_value = install_status
        fake_package.uninstall.return_value = uninstall_status
        import_mock.Formula.return_value = fake_package

        return filenames, import_mock

    def test_available_packages_valid_files(self):
        filenames, import_mock = self.create_fake_import(name=FAKE_NAME1)

        with patch('procyon.pkg.logic.os.listdir', new=lambda ls: filenames):
            with patch('__builtin__.__import__', new=lambda *args: import_mock):
                packages = get_available_packages()

        self.assertEqual(len(packages), 1)
        self.assertTrue(FAKE_NAME1 in packages)

    def test_available_packages_missed_attr(self):
        filenames, import_mock = self.create_fake_import(name=FAKE_NAME1, check_items=False)

        with patch('procyon.pkg.logic.os.listdir', new=lambda ls: filenames):
            with patch('__builtin__.__import__', new=lambda *args: import_mock):
                packages = get_available_packages()

        self.assertFalse(packages)

    def test_available_packages_invalid_files(self):
        filenames = [
            '__ini__.py',
            'module.pyc',
        ]

        with patch('procyon.pkg.logic.os.listdir', new=lambda ls: filenames):
            packages = get_available_packages()

        self.assertFalse(packages)

    def test_available_packages_by_name(self):
        filenames, import_mock = self.create_fake_import(name=FAKE_NAME1)

        with patch('procyon.pkg.logic.os.listdir', new=lambda ls: filenames):
            with patch('__builtin__.__import__', new=lambda *args: import_mock):
                packages = get_available_packages_by_name(name=FAKE_NAME1)

                self.assertEqual(len(packages), 1)
                self.assertTrue(FAKE_NAME1 in packages)

                packages = get_available_packages_by_name(name='not_founded')

                self.assertFalse(packages)

    def test_outdated_packages(self):
        available_version = '2'
        filenames, import_mock = self.create_fake_import(name=FAKE_NAME1, version=available_version)

        with patch('procyon.pkg.logic.Package', new=FakePackage):
            with patch('procyon.pkg.logic.os.listdir', new=lambda ls: filenames):
                with patch('__builtin__.__import__', new=lambda *args: import_mock):
                    packages = get_outdated_packages()

        self.assertEqual(type(packages), type({}))
        self.assertEqual(len(packages), 1)
        self.assertTrue(FAKE_NAME1 in packages)

        package = packages.get(FAKE_NAME1)
        self.assertEqual(package.get('available_version'), available_version)
        self.assertEqual(package.get('version'), FakePackage.get(name=FAKE_NAME1).version)

    def test_compare_versions(self):
        test_cases = (
            ('1.4.2', '1.2'),
            ('10.0', '9.9'),
            ('11', '10.9.9.9'),
            ('11.0.0.1', '11'),
            ('0.1', '0.0.1'),
        )
        for case in test_cases:
            self.assertTrue(check_version(case[0], case[1]))
            self.assertFalse(check_version(case[1], case[0]))

    def test_install_ok(self):
        p = FakePackage.get(name=FAKE_NAME1)
        p.delete_instance()
        filenames, import_mock = self.create_fake_import(name=FAKE_NAME1)
        packages_count = FakePackage.select().count()

        with patch('procyon.pkg.logic.os.listdir', new=lambda ls: filenames):
            with patch('__builtin__.__import__', new=lambda *args: import_mock):
                status = install_package(FAKE_NAME1)

        self.assertEqual(status, InstallationStatuses.INSTALL_OK)
        self.assertEqual(FakePackage.select().count(), packages_count + 1)

    def test_install_already_installed(self):
        filenames, import_mock = self.create_fake_import(name=FAKE_NAME1)
        packages_count = FakePackage.select().count()

        with patch('procyon.pkg.logic.os.listdir', new=lambda ls: filenames):
            with patch('__builtin__.__import__', new=lambda *args: import_mock):
                status = install_package(FAKE_NAME1)

        self.assertEqual(status, InstallationStatuses.ALREADY_INSTALLED)
        self.assertEqual(FakePackage.select().count(), packages_count)

    def test_install_error(self):
        p = FakePackage.get(name=FAKE_NAME1)
        p.delete_instance()
        filenames, import_mock = self.create_fake_import(name=FAKE_NAME1, install_status=InstallationStatuses.INSTALL_ERROR)
        packages_count = FakePackage.select().count()

        with patch('procyon.pkg.logic.os.listdir', new=lambda ls: filenames):
            with patch('__builtin__.__import__', new=lambda *args: import_mock):
                status = install_package(FAKE_NAME1)

        self.assertEqual(status, InstallationStatuses.INSTALL_ERROR)
        self.assertEqual(FakePackage.select().count(), packages_count)

    def test_uninstall_ok(self):
        filenames, import_mock = self.create_fake_import(name=FAKE_NAME1)
        packages_count = FakePackage.select().count()

        with patch('procyon.pkg.logic.os.listdir', new=lambda ls: filenames):
            with patch('__builtin__.__import__', new=lambda *args: import_mock):
                status = uninstall_package(FAKE_NAME1)

        self.assertEqual(status, InstallationStatuses.UNINSTALL_OK)
        self.assertEqual(FakePackage.select().count(), packages_count - 1)

    def test_uninstall_error(self):
        filenames, import_mock = self.create_fake_import(name=FAKE_NAME1, uninstall_status=InstallationStatuses.UNINSTALL_ERROR)
        packages_count = FakePackage.select().count()

        with patch('procyon.pkg.logic.os.listdir', new=lambda ls: filenames):
            with patch('__builtin__.__import__', new=lambda *args: import_mock):
                status = uninstall_package(FAKE_NAME1)

        self.assertEqual(status, InstallationStatuses.UNINSTALL_ERROR)
        self.assertEqual(FakePackage.select().count(), packages_count)


if __name__ == '__main__':
    unittest.main()
