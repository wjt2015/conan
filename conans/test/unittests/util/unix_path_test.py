#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import platform
import unittest

from conans.client import tools
from conans.client.tools.win import get_cased_path
from conans.test.utils.test_files import temp_folder
from conans.util.files import mkdir


class GetCasedPath(unittest.TestCase):
    @unittest.skipUnless(platform.system() == "Windows", "Requires Windows")
    def test_case_existing(self):
        folder = get_cased_path(temp_folder())
        p1 = os.path.join(folder, "MyFolder", "Subfolder")
        mkdir(p1)

        self.assertEqual(p1, get_cased_path(p1))  # Idempotent
        self.assertEqual(p1, get_cased_path(os.path.join(folder, "myfolder", "subfolder")))

    def test_case_not_existing(self):
        current_dir = get_cased_path(os.getcwd())
        non_existing_path = os.path.join(current_dir, "this", "Path", "does", "NOT", "Exists")
        p = get_cased_path(non_existing_path)  # If not exists from the root, returns as is
        self.assertEqual(p, non_existing_path)

    @unittest.skipUnless(platform.system() == "Windows", "Requires Windows")
    def test_case_partial_exists(self):
        folder = get_cased_path(temp_folder())
        p1 = os.path.join(folder, "MyFolder", "Subfolder")
        mkdir(p1)

        non_existing_path = os.path.join(folder, "myfolder", "subfolder", "not-existing")
        # The first part of the path will be properly cased.
        self.assertEqual(os.path.join(p1, "not-existing"),
                         get_cased_path(non_existing_path))


class UnixPathTest(unittest.TestCase):

    def test_none(self):
        self.assertEqual(None, tools.unix_path(path=None))

    @unittest.skipIf(platform.system() == "Windows", "All but Windows")
    def test_not_windows(self):
        path = 'C:\\Windows\\System32'
        self.assertEqual(path, tools.unix_path(path))

    @unittest.skipUnless(platform.system() == "Windows", "Only windows")
    def test_msys_path(self):
        self.assertEqual('/c/windows/system32', tools.unix_path('C:\\Windows\\System32',
                                                                path_flavor=tools.MSYS2))

    @unittest.skipUnless(platform.system() == "Windows", "Only windows")
    def test_cygwin_path(self):
        self.assertEqual('/cygdrive/c/windows/system32', tools.unix_path('C:\\Windows\\System32',
                                                                         path_flavor=tools.CYGWIN))

    @unittest.skipUnless(platform.system() == "Windows", "Only windows")
    def test_wsl_path(self):
        self.assertEqual('/mnt/c/Windows/System32', tools.unix_path('C:\\Windows\\System32',
                                                                    path_flavor=tools.WSL))

    @unittest.skipUnless(platform.system() == "Windows", "Only windows")
    def test_sfu_path(self):
        self.assertEqual('/dev/fs/C/windows/system32', tools.unix_path('C:\\Windows\\System32',
                                                                       path_flavor=tools.SFU))
