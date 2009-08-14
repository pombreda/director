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
Unittests.
"""

import glob
import os.path

from unittest import TestLoader


TESTFILES = []
for t in glob.glob(os.path.join('tests', '*.py')):
    if not t.endswith('__init__.py'):
        TESTFILES.append('.'.join(
            ['tests', os.path.splitext(os.path.basename(t))[0]]))

TESTS = TestLoader().loadTestsFromNames(TESTFILES)
