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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import websocket
import json
import logging
import base64
import sys
import random

try:
    from pyBluzelle.proto import bluzelle_pb2
    from pyBluzelle.proto import database_pb2
except ImportError as e:
    raise ImportError("{}\n\nTo generate Bluzelle protobuf modules:\n"
                      "\n"
                      "$ protoc --python_out=./pyBluzelle/proto --proto_path=proto/proto bluzelle.proto database.proto audit.proto\n".format(e.message))

logger = logging.getLogger(__name__)


class Connection(object):

    def __init__(self, host, port, uuid):
        """
        Create a connection to a Bluzelle database
        :param host: hostname for the Bluzelle node
        :param port: port of the Bluzelle node
        :param uuid: uuid of the database to connect
        """
        self._host = host
        self._port = port
        self._uuid = uuid
        self._transaction_id_map = {}
        self._connect(host, port)

    def _connect(self, host, port, timeout=1):
        self._ws = websocket.create_connection("ws://{}:{}".format(host, port))
        self._ws.settimeout(timeout)

    def _send_request_async(self, msg):
        pass

    def _send_request_sync(self, msg):
        msg.db.header.db_uuid = self._uuid
        msg.db.header.transaction_id = random.randint(1, sys.maxsize)

        req = {}
        req["bzn-api"] = "database"
        req["msg"] = base64.b64encode(msg.SerializeToString()).decode()

        logger.debug("Sending: {}".format(msg))
        self._ws.send(json.dumps(req))
        response = self.read_response(msg)
        return response

    def read_response(self, msg=None):
        resp = database_pb2.database_response()
        resp.ParseFromString(self._ws.recv())

        if resp.WhichOneof('response') == 'redirect':
            host = resp.redirect.leader_host
            port = resp.redirect.leader_port
            self._connect(host, port)
            logger.debug("redirecting to leader at {}:{}.\n".format(host, port))
            resp = self._send_request_sync(msg)
        else:
            logger.debug("Response: \n{}".format(resp))
        return resp

    def create(self, key, value):
        """
        Create a new K/V
        :param key: New key to create
        :param value: New value to add to the key
        :return:
        """
        msg = bluzelle_pb2.bzn_msg()
        msg.db.create.key = key
        msg.db.create.value = value
        self._send_request_sync(msg)

    def read(self, key):
        """
        Read a value at a key
        :param key: Key to read
        :return: value
        """
        msg = bluzelle_pb2.bzn_msg()
        msg.db.read.key = key
        resp = self._send_request_sync(msg)
        return resp.read.value

    def update(self, key, value):
        """
        Update a K/V
        :param key: Key to update
        :param value: Value to update
        :return:
        """
        msg = bluzelle_pb2.bzn_msg()
        msg.db.update.key = key
        msg.db.update.value = value
        self._send_request_sync(msg)

    def delete(self, key):
        """
        Create a new K/V
        :param key: Key to delete
        :return:
        """
        msg = bluzelle_pb2.bzn_msg()
        msg.db.delete.key = key
        self._send_request_sync(msg)

    def has(self, key):
        """
        Create a new K/V
        :param key: Key to test
        :return: true if key exists
        """
        msg = bluzelle_pb2.bzn_msg()
        msg.db.has.key = key
        resp = self._send_request_sync(msg)
        return resp.has.has

    def keys(self):
        """
        Query for all keys in a database
        :return: List of keys in the database
        """
        msg = bluzelle_pb2.bzn_msg()
        msg.db.keys.SetInParent()
        resp = self._send_request_sync(msg)
        return resp.keys.keys

    def size(self):
        """
        Query for size of the database in bytes
        :return: Size of the database in bytes
        """
        msg = bluzelle_pb2.bzn_msg()
        msg.db.size.SetInParent()
        resp = self._send_request_sync(msg)
        return ({"bytes": resp.size.bytes,
                 "keys": resp.size.keys})

    def subscribe(self):
        logger.info("Command not implement")
        return

    def unsubscribe(self):
        logger.info("Command not implement")
        return
