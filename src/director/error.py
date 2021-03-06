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
Exception classes.
"""

__docformat__ = 'restructuredtext'


class DirectorError(Exception):
    """
    Base class for Director specific exceptions.
    """
    pass


class UnsuportedHelpStyleError(DirectorError):
    """
    Used when an unsupported help style is attempted.
    """
    pass
