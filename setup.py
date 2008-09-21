#!/usr/bin/env python
#
# Copyright 2008, Red Hat, Inc
# Steve 'Ashcrow' Milner <smilner@redhat.com>
#
# This software may be freely redistributed under the terms of the GNU
# general public license.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
Standard build script.
"""

import sys
import os
from glob import glob
from distutils.core import Command, setup
from unittest import TextTestRunner, TestLoader
from os.path import basename, walk, splitext
from os.path import join as pjoin

sys.path.insert(0, 'src')
sys.path.insert(1, 'tests')

from director import __version__
from director import __license__


class DocCommand(Command):
    """
    Documentation generation command.
    """
    user_options = []

    def initialize_options(self):
        """
        Setup the current dir.
        """
        self._dir = os.getcwd()

    def finalize_options(self):
        """
        No clue ... but it's required.
        """
        pass

    def run(self):
        """
        Creates HTML documentation using epydoc.
        """
        print "Creating html documentation ..."

        try:
            from epydoc.docbuilder import build_doc_index
            from epydoc.docwriter.html import HTMLWriter

            docidx = build_doc_index([os.path.join('src', 'director/')])
            html_writer = HTMLWriter(docidx,
                                     prj_name = 'director',
                                     prj_url = '')
            html_writer.write(os.path.join('docs'))
        except:
            print >> sys.stderr, "You don't seem to have the following which"
            print >> sys.stderr, "are required to make documentation:"
            print >> sys.stderr, "\tepydoc.docbuilder.build_doc_index"
            print >> sys.stderr, "\tepydoc.docwriter.html.HTMLWriter"
            print >> sys.stderr, "Trying running from the command line ..."
            try:
                if os.system('epydoc -o docs src') != 0:
                    raise
            except:
                print >> sys.stderr, "FAIL! exiting ..."
                sys.exit(1)

        print "Your docs are now in docs"


class TestCommand(Command):
    """
    Distutils testing command.
    """
    user_options = []

    def initialize_options(self):
        """
        Setup the current dir.
        """
        self._dir = os.getcwd()

    def finalize_options(self):
        """
        No clue ... but it's required.

        @param self: Internal Command object.
        @type self: Command
        """
        pass

    def run(self):
        """
        Finds all the tests modules in tests/, and runs them.
        """
        testfiles = []
        for t in glob(pjoin(self._dir, 'tests', '*.py')):
            if not t.endswith('__init__.py'):
                testfiles.append('.'.join(
                    ['tests', splitext(basename(t))[0]]))

        tests = TestLoader().loadTestsFromNames(testfiles)
        t = TextTestRunner(verbosity = 2)
        t.run(tests)


setup(name = "director",
    version = __version__,
    description = "Command line plugin library",
    author = 'Steve Milner',
    author_email = 'smilner@redhat.com',

    license = __license__,

    package_dir = {'director': 'src/director'},
    packages = ['director'],

    classifiers=[
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python'],

    cmdclass = {'test': TestCommand,
                'doc': DocCommand})
