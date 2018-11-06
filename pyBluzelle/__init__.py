# Copyright (C) 2018 Bluzelle
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License, version 3,
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from pyBluzelle.communication import Connection
import logging
from .version import get_version

__version__ = get_version()


def create_connection(host, port, uuid):

    return Connection(host, port, uuid)

# Be nice and set up logging to /dev/null
class NullHandler(logging.Handler):
    def emit(self, record):
        pass

log = logging.getLogger('pyBluzelle')
log.addHandler(NullHandler())
