#!/usr/bin/env python3
""" Test utilities for execution of third party tools """

import unittest
import tempfile
import os

from sjcb.utils import exe

class RunShellCommand(unittest.TestCase):
    """ Test simple invocations """
    def setUp(self):
        self.tmpfile = tempfile.mkstemp()
    def tearDown(self):
        os.remove(self.tmpfile[1])

    def test_echo_foo(self):
        (stdout, stderr, rc) = exe.run_shell_command("echo foo")

        self.assertIsInstance(stdout, str)
        self.assertIsInstance(stderr, str)
        self.assertIsInstance(rc, int)

        self.assertEqual(stdout, 'foo\n')
        self.assertEqual(stderr, '')
        self.assertEqual(rc, 0)

    def test_command_not_found(self):
        (stdout, stderr, rc) = exe.run_shell_command("blah")

        self.assertEqual(rc, 127)

    def test_shell_true(self):
        (stdout, stderr, rc) = exe.run_shell_command("echo foo && echo bar", shell=True)

        self.assertEqual(stdout, 'foo\nbar\n')
        self.assertEqual(stderr, '')
        self.assertEqual(rc, 0)

    def test_bad_ls(self):
        (stdout, stderr, rc) = exe.run_shell_command("ls blah")

        self.assertEqual(stdout, '')
        self.assertEqual(stderr, "ls: cannot access 'blah': No such file or directory\n")
        self.assertEqual(rc, 2)

    def test_redirect_stdout(self):
        fout = open(self.tmpfile[1], 'w')
        (stdout, stderr, rc) = exe.run_shell_command("echo foo", stdout=fout)
        fout.close()

        lines = []
        with open(self.tmpfile[0]) as fp:
            lines.append(fp.readline())

        self.assertEqual(lines, ['foo\n'])
        self.assertEqual(stdout, '')
        self.assertEqual(stderr, '')
        self.assertEqual(rc, 0)

    def test_redirect_stderr(self):
        ferr = open(self.tmpfile[1], 'w')
        (stdout, stderr, rc) = exe.run_shell_command("ls blah", stderr=ferr)
        ferr.close()

        lines = []
        with open(self.tmpfile[0]) as fp:
            lines.append(fp.readline())

        self.assertEqual(lines, ["ls: cannot access 'blah': No such file or directory\n"])
        self.assertEqual(stdout, '')
        self.assertEqual(stderr, '')
        self.assertEqual(rc, 2)



