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
Main classes for director.
"""

import os
import sys
import types

__version__ = '1.1.0'
__license__ = 'GPLv3+'


class Action(object):
    """
    Base class for command line actions.
    """

    description_txt = "Base action class"

    def __init__(self):
        """
        Create the Action object. Do not override.
        """
        self._startup_hook()

    def __del__(self):
        """
        Work to do when the object is deleted. Do not override.
        """
        self._shutdown_hook()

    def __repr__(self):
        """
        String representation of the object.
        """
        return "<%s Action>" % self.__class__.__name__

    def _startup_hook(self):
        """
        Hook for doing work on creation of the object. It's not in
        __init__ just so that we keep __init__ clean.
        """
        pass

    def _shutdown_hook(self):
        """
        Hook for doing work on deletion of the object. It's not in
        __del__ just so that we keep __del__ clean.
        """
        pass

    def _list_verbs(self):
        """
        Lists all available verbs.
        """
        verbs = []
        for item in dir(self):
            if item[0] != '_':
                if type(self.__getattribute__(item)) == types.MethodType:
                    verbs.append(item)
        return verbs

    def _action_help(self):
        """
        Formats and shows help for all available verbs in an action.
        """
        print >> sys.stderr, "Usage: myapp [verb] [--opt=val]..."
        print >> sys.stderr, "%s\n" % self.description_txt
        for verb in self._list_verbs():
            print >> sys.stderr, "%s -" % verb,
            self.help(verb)
            print >> sys.stderr, "\n"

    def help(self, verb=None):
        """
        Detailed help information about the action.

        == help ==
        \nOptions:
        \tverb:\tverb to get help on

        Example:
        \tmyapp list help --verb=help
        == end help ==

        Do not override.

        @param verb: The verb to get help on
        @type verb: str
        """
        # If we have no verb then show help for everything
        if not verb:
            self._action_help()
            return

        base_doc_string = True # signifies we are in the general area
        in_help = False # signifies if we are in the == help == area
        doc_string = self.__getattribute__(verb).__doc__.replace("    ", "")
        # For each line in the doc string see if we should print the info
        for line in doc_string.split('\n')[1:]:
            # If we have a blank line AND we are not in the help section ..
            if line == '' and not in_help:
                base_doc_string = False
            # Print base doc string data
            if base_doc_string:
                print >> sys.stderr, line
            # If we see == help == say we are in == help == section
            if '== help ==' in line:
                in_help = True
            # If we see == end help == we are out of the help section
            elif '== end help ==' in line:
                in_help = False
            # Print all lines that are in the help section
            elif in_help:
                print >> sys.stderr, line

    def description(self):
        """
        Quick blurb about the action.

        == help ==
        \nOptions:
        \tNone

        Example:
        \tmyapp list description
        == end help ==

        Do not override. See description_txt
        """
        verbs = ", ".join(self._list_verbs())
        print >> sys.stderr, "%s. Available verbs: %s" % (self.description_txt, verbs)


class ActionRunner(object):
    """
    In charge of running plugins based on information passed in via arguments.
    """

    def __init__(self, args, plugin_package):
        """
        Creates the ActionRunner object.

        @param args: all args passed from command line
        @type args: list

        @params plugin_package: The package where plugins live
        @type plugin_package: str
        """
        self.plugin_package = plugin_package

        if not len(args[1:]) >= 2:
            self.__list_nouns()
            print >> sys.stderr, "Please give at least a noun and a verb."
            sys.exit(1)
        # Get all the options passed in
        self.noun, self.verb = args[1:3]
        self.options = self.parse_options(args[3:])

        # Generate the code based from the input
        action = __import__("%s.%s" % (self.plugin_package, self.noun))
        for drop_x in range(self.plugin_package.count('.')):
            drop_x += 1
            actions = action.__getattribute__(
                self.plugin_package.split('.')[drop_x])
        module = actions.__getattribute__(self.noun)
        self.action_to_run = module.__getattribute__(self.noun.capitalize())()

    def __list_nouns(self):
        """
        Lists all available nouns.
        """
        action_mod = __import__(self.plugin_package)
        print >> sys.stderr, "Available nouns:",
        # Get the module path from __path__ of action_mod and plugin_package
        mod_path = os.path.join(action_mod.__path__[0],
                                self.plugin_package.split('.')[-1])
        # Go over each and print out the ones that are actions
        for noun in os.listdir(mod_path):
            if "__" not in noun and '.pyc' not in noun:
                print >> sys.stderr, "%s " % noun.replace('.py', ''),
        print >> sys.stderr, ""

    def parse_options(self, options):
        """
        Parse the options into something that can be passed to a method.

        @param options: The options passed in
        @type options: list

        @return: A usable dictionary to pass to a method
        @rtype: dict
        """
        method_dict = {}
        for option in options:
            if option.count('=') > 0:
                key, value = option.split('=')
            else:
                key = option
                value = True
            key = key.replace('--', '').replace('-', '_')
            method_dict[key] = value
        return method_dict

    def run_code(self):
        """
        Takes care of running the code created.

        @param code: The code to execute
        @type code: str
        """
        self.action_to_run.__getattribute__(
            self.verb).__call__(**self.options)

    def run(self, filter_obj=None):
        """
        Runs the generated code.

        @param filter_obj: The filter object
        @type error_str: Filter
        """
        try:
            self.run_code()
        except Exception, ex:
            if filter_obj:
                filter_obj.execute_filters(ex)
            sys.exit(1)
