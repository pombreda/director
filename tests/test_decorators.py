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
Test of director decorators.
"""

import exceptions
import inspect
import types
import unittest

from director import decorators


class Fake(object):

    @decorators.help("Test of help")
    def method(self, input):
        return input


class ActionTests(unittest.TestCase):
    """
    Tests to verify that base action class works correctly.
    """

    def setUp(self):
        """
        Sets up stuff for the test.
        """
        self.fake_obj = Fake()

    def test_help(self):
        """
        Make sure that the test decorator works as expected.
        """
        self.assertEqual(self.fake_obj.method.help, "Test of help")
        self.assertEqual(type(self.fake_obj.method.meth), types.FunctionType)
        self.assertEqual(inspect.getargspec(self.fake_obj.method.meth)[0],
                         ['self', 'input'])
