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
Test action to use in unit tests.
"""

import director


class Simpleaction(director.Action):
    """
    Very simple action for use in testing.
    """

    def verb(self, opt, another=False, last="last"):
        """
        An example verb.

        == help ==
        \nOptions:
        \topt:\tsome kind of option

        Example:
        \tmyapp simpleaction verb --opt=something

        == end help ==
        """
        pass
