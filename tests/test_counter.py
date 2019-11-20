# -*- coding: utf-8 -*-
# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Counter Model

Test cases can be run with:
  python -m unittest discover
  nosetests
  coverage report -m
  nosetests --stop tests/test_counter.py:CounterTests
"""

import os
import logging
from unittest import TestCase
from unittest.mock import patch
from redis.exceptions import ConnectionError
from service.models import Counter, DatabaseConnectionError

logging.disable(logging.CRITICAL)

DATABASE_URI = os.getenv("DATABASE_URI", "redis://:@localhost:6379/0")


class CounterTests(TestCase):
    def setUp(self):
        self.counter = Counter()

    def tearDown(self):
        Counter.reset_credentials()

    def test_create_counter_with_name(self):
        """ Create a counter with a name """
        counter = Counter("foo")
        self.assertIsNotNone(counter)
        self.assertEqual(counter.name, "foo")

    def test_create_counter_no_name(self):
        """ Create a counter without a name """
        self.assertIsNotNone(self.counter)
        self.assertEqual(self.counter.name, "hits")

    def test_credential_initialization(self):
        """ Make sure credentials are initialized """
        credentials = Counter.credentials
        self.assertEqual(credentials["prefix"], "")
        self.assertEqual(credentials["userid"], "")
        self.assertEqual(credentials["password"], "")
        self.assertEqual(credentials["host"], "")
        self.assertEqual(credentials["port"], 0)
        self.assertEqual(credentials["database"], "")

    def test_set_get_counter(self):
        """ Set and then Get the counter """
        self.counter.connect(DATABASE_URI)
        self.counter.value = 13
        self.assertEqual(self.counter.value, 13)

    def test_delete_counter(self):
        """ Delete a counter """
        self.counter.connect(DATABASE_URI)
        del self.counter.value
        self.assertEqual(self.counter.value, 0)

    def test_increment_counter(self):
        """ Increment the current value of the counter by 1 """
        self.counter.connect(DATABASE_URI)
        count = self.counter.value
        next_count = self.counter.increment()
        logging.debug(
            "count(%s) = %s, next_count(%s) = %s",
            type(count),
            count,
            type(next_count),
            next_count,
        )
        self.assertEqual(next_count, count + 1)

    def test_parse_uri(self):
        """ Make sure uri populates credentials """
        self.counter.parse_uri("redis://admin:pass@localhost:6379/0")
        credentials = Counter.credentials
        self.assertEqual(credentials["prefix"], "redis:")
        self.assertEqual(credentials["userid"], "admin")
        self.assertEqual(credentials["password"], "pass")
        self.assertEqual(credentials["host"], "localhost")
        self.assertEqual(credentials["port"], 6379)
        self.assertEqual(credentials["database"], "0")

    def test_missing_creds(self):
        """ Check for missing credentials """
        self.counter.parse_uri("redis://:@localhost:6379/0")
        credentials = Counter.credentials
        self.assertEqual(credentials["prefix"], "redis:")
        self.assertEqual(credentials["userid"], "")
        self.assertEqual(credentials["password"], "")
        self.assertEqual(credentials["host"], "localhost")
        self.assertEqual(credentials["port"], 6379)
        self.assertEqual(credentials["database"], "0")

    def test_create_counter_no_port(self):
        """ URI with missing port """
        self.assertRaises(
            DatabaseConnectionError, self.counter.parse_uri, "redis://:@localhost:/0"
        )

    def test_create_counter_bad_port(self):
        """ URI with bad port data """
        self.assertRaises(
            DatabaseConnectionError, self.counter.parse_uri, "redis://:@localhost:foo/0"
        )

    def test_create_counter_no_host(self):
        """ URI with no hostname """
        self.assertRaises(
            DatabaseConnectionError, self.counter.parse_uri, "redis://:@:6379foo/0"
        )

    def test_connection(self):
        """ Make sure connection is working """
        self.counter.connect(DATABASE_URI)
        credentials = Counter.credentials
        self.assertEqual(credentials["prefix"], "redis:")
        self.assertEqual(credentials["userid"], "")
        self.assertEqual(credentials["password"], "")
        self.assertEqual(credentials["host"], "localhost")
        self.assertEqual(credentials["port"], 6379)
        self.assertEqual(credentials["database"], "0")

    @patch("redis.Redis.ping")
    def test_no_connection(self, ping_mock):
        """ Handle failed connection """
        ping_mock.side_effect = ConnectionError()
        self.assertRaises(DatabaseConnectionError, self.counter.connect, DATABASE_URI)

    @patch.dict(os.environ, {"DATABASE_URI": "redis://:@localhost:6379/0"})
    def test_environment_uri(self):
        """ Get DATABASE_URI from environment """
        self.counter.connect()
        credentials = Counter.credentials
        self.assertEqual(credentials["prefix"], "redis:")
        self.assertEqual(credentials["userid"], "")
        self.assertEqual(credentials["password"], "")
        self.assertEqual(credentials["host"], "localhost")
        self.assertEqual(credentials["port"], 6379)
        self.assertEqual(credentials["database"], "0")

    @patch.dict(os.environ, {"DATABASE_URI": ""})
    def test_missing_environment_creds(self):
        """ Missing environment credentials """
        self.assertRaises(DatabaseConnectionError, self.counter.connect)
