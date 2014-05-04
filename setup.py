#!/usr/bin/env python

from distutils.core import setup

from setuptools.command.test import test as TestCommand
import sys

class Tox(TestCommand):
    def finalize_options(self):
        super(Tox, self).finalize_options(self)
        self.test_args = []
        self.test_suite = True
    
    def run_test(self):
        import tox
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)

setup(
    name='eHacktivities',
    version='1.0',
    description='eActivities Screen-Scraping API',
    author='Luke Granger-Brown',
    author_email='git@lukegb.com',
    packages=['eactivities'],
    tests_require=['tox'],
    cmdclass = {'test': Tox},
)
