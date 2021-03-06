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
Test for director
"""

__docformat__ = 'restructuredtext'


import exceptions
import inspect
import os
import sys
import tempfile
import unittest

from director.filter import Filter
from director.filter import ExceptionFilter


STDOUT = sys.stdout
STDERR = sys.stderr
TMP = tempfile.mkstemp()[1]


class ErrTests(unittest.TestCase):
    """
    Test the err function.
    """

    def setUp(self):
        """
        Import err as self.err for the test.
        """
        import sys
        from director import err
        self.err = err
        sys.stdout = open(TMP, 'w')
        sys.stderr = open(TMP, 'w')

    def tearDown(self):
        """
        Moves streams back to their right place.
        """
        sys.stdout.close()
        sys.stdout = STDOUT
        sys.stderr = STDERR

    def test__err_spec(self):
        """
        Make sure the inputs to the function are what we expect.
        """
        spec = inspect.getargspec(self.err)
        # Check general spec
        self.assertEquals(spec.args, ['text', 'newline'])
        self.assertRaises(TypeError, self.err)

    def test__err_with_strings(self):
        """
        Test the err funtion with string input.
        """
        self.err('ok')
        self.err('ok', False)
        self.err('this is a longer string')
        self.err('this is a longer string', False)
        self.err(unicode('this is a unicode string'))
        self.err(unicode('this is a unicode string'), False)
        self.err('123123123123123')
        self.err('123123123123123', False)

    def test__err_with_numbers(self):
        """
        Test the err funtion with numerical input.
        """
        self.err(1)
        self.err(1, False)
        self.err(123482983748923749723984728934789237489)
        self.err(123482983748923749723984728934789237489, False)
        self.err(1000000*10000000)
        self.err(1000000*10000000, False)
        self.err(long(123123))
        self.err(long(123123), False)
        self.err(1e100)
        self.err(1e100, False)

    def test__err_with_objects(self):
        """
        Test the err funtion with object input.
        """
        self.err(['one', 'two', 'three'])
        self.err(['one', 'two', 'three'])
        self.err({'ok': 'hi', 'fine': 'there'})
        self.err({'ok': 'hi', 'fine': 'there'})
        self.err(object())
        self.err(object(), False)
        self.err(object)
        self.err(object, False)


class ActionTests(unittest.TestCase):
    """
    Tests to verify that base action class works correctly.
    """

    def setUp(self):
        """
        Sets up stuff for the test.
        """
        import sys
        from director import Action

        # Remap stdout for these tests
        self.action = Action()
        sys.stdout = open(TMP, 'w')
        sys.stderr = open(TMP, 'w')

    def tearDown(self):
        """
        Tears down stuff for config test.
        """
        del self.action
        # Map the original stdout/stderr back
        sys.stdout.close()
        sys.stdout = STDOUT
        sys.stderr = STDERR

    def test__list_verbs(self):
        """
        Tests the _list_verbs method.
        """
        self.assertEqual(self.action._list_verbs(), ['description', 'help'])

    def test__list_verbs(self):
        """
        Tests the _list_verbs method.
        """
        self.assertEqual(self.action._list_verbs(), ['description', 'help'])

    def test_description(self):
        """
        Tests the description works.
        """
        self.action.description()

    def test_help(self):
        """
        Tests the help works.
        """
        self.action.help()
        self.action.help('help')

    def test__action_help(self):
        """
        Tests the _action_help works.
        """
        self.action._action_help()


class ActionRunnerTests(unittest.TestCase):
    """
    Tests to verify base ActionRunner class works as expected.
    """

    def setUp(self):
        """
        Sets up stuff for the test.
        """
        from director import ActionRunner

        self.arunner = ActionRunner(['self', 'simpleaction',
                                     'verb', '--opt=value', '--another'],
                                    'tests.actions')

    def test_parse_options(self):
        """
        Make sure the parsing of options works.
        """
        res = self.arunner.parse_options()
        self.assertEqual(res, {'opt': 'value',
                               'another': False,
                               'last': 'last'})

    def test_run_code(self):
        """
        Verify generated code runs.
        """
        self.arunner.run_code()

    def test_run_with_filter(self):
        """
        Verify generated code runs with filter.
        """
        filter = Filter()
        filter.register_filter(ExceptionFilter(exceptions.IOError, ''))
        self.arunner.verb = 'verb'
        self.arunner.options = {'opt': 'ok'}
        self.arunner.run(filter)

    def test_run_without_filter(self):
        """
        Verify generated code runs without filter.
        """
        self.arunner.run()

    def test_run_execption_without_filter(self):
        """
        Verify generated raises an exception if there are no filters
        during run.
        """
        self.arunner.verb = "asdasd"
        self.assertRaises(AttributeError, self.arunner.run)
