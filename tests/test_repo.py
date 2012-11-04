#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest

from git.exc import InvalidGitRepositoryError
from mock import patch, MagicMock

from procyon.repo.logic import update_repo


__all__ = (
    'LogicTests',
)


def raise_invalid_git_repo_error(*args, **kwargs):
    raise InvalidGitRepositoryError


class LogicTests(unittest.TestCase):
    @patch('procyon.repo.logic.GitRepo', new=MagicMock)
    def test_ok_update(self):
        result = update_repo()

        self.assertTrue(result[0])
        self.assertNotEquals(result[1], None)
        self.assertNotEquals(result[2], None)

    def test_fail_update(self):
        with patch('procyon.repo.logic.GitRepo', new=raise_invalid_git_repo_error):
            result = update_repo()

            self.assertEquals(result, (False, None, None))


if __name__ == '__main__':
    unittest.main()
