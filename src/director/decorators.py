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
All decorators for director.
"""


def help(help_txt):
    """
    Adds a help variable to a class method as well as saving the original
    method as meth.

    help is the text to add as help text.
    """

    def decorator(meth):
        """
        Top level inner decorator which takes in a class method.

        meth is the actual class method.
        """

        def wrapper(self, *args, **kwargs):
            """
            Internal wrapper that actually executes the method.

            self is the class methods container object.
            *args are any non keyword arguments.
            **kwargs are all keyword arguments.
            """
            return meth(self, *args, **kwargs)

        # Add help variable and it's text
        wrapper.help = help_txt
        # Attach the original method as meth for inspection
        wrapper.meth = meth
        return wrapper

    return decorator
