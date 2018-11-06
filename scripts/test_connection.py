#!/usr/bin/env python2.7
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

import pyBluzelle


if __name__ == '__main__':

    b = pyBluzelle.create_connection("testnet.bluzelle.com", 51010, "137a8403-52ec-43b7-8083-91391d4c5e67")
    res = b.has(b"kk")
    print(res)
    res = b.create(b"kk", b"1234")
    print(res)
    res = b.create(b"gg", b"1234")
    print(res)
    res = b.keys()
    print(res)
    res = b.read(b"gg")
    print(res)
    res = b.has(b"gg")
    print(res)
    res = b.delete(b"gg")
    print(res)
    res = b.keys()
    print(res)
    res = b.size()
    print(res)
    res = b.read(b"gg")
    print(res)
    res = b.delete(b"kk")
    print(res)
