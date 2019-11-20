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
Test cases for Counter Service

Test cases can be run with:
  python -m unittest discover
  nosetests
  coverage report -m
  nosetests --stop tests/test_service.py:ServiceTest
"""
import os
import logging
from unittest import TestCase
from unittest.mock import patch
import service

DATABASE_URI = os.getenv("DATABASE_URI", "redis://:@localhost:6379/0")


class ServiceTest(TestCase):
    def setUp(self):
        service.app.debug = False
        service.service.DATABASE_URI = DATABASE_URI
        self.app = service.app.test_client()

    def test_index(self):
        """ Get the home page """
        resp = self.app.get("/")
        self.assertEquals(resp.status_code, 200)

    def test_get_counter(self):
        """ Get the counter """
        resp = self.app.get("/counter")
        self.assertEquals(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["counter"] is not None)

    def test_increment_counter(self):
        """ Increment the counter """
        resp = self.app.get("/counter")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        count = int(data["counter"])

        # post and make sure the counter is increments
        resp = self.app.post("/counter")
        self.assertEqual(resp.status_code, 201)
        resp = self.app.post("/counter")
        self.assertEqual(resp.status_code, 201)

        # check that it was incremented by 2
        data = resp.get_json()
        new_count = int(data["counter"])
        self.assertEqual(new_count, count + 2)

    def test_reset_the_counter(self):
        # post and make sure the counter is increments
        resp = self.app.post("/counter")
        self.assertEqual(resp.status_code, 201)
        resp = self.app.post("/counter")
        self.assertEqual(resp.status_code, 201)

        # make sure the counter is not zero
        resp = self.app.get("/counter")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        count = int(data["counter"])
        self.assertGreater(count, 0)

        # now reset the counter to zero
        data = {"counter": 0}
        resp = self.app.put("/counter", json=data)
        self.assertEqual(resp.status_code, 200)
        new_data = resp.get_json()
        new_count = int(new_data["counter"])
        self.assertEquals(new_count, 0)

    ######################################################################
    #  T E S T   E R R O R   H A N D L E R S
    ######################################################################

    # @patch('service.models.Counter.value')
    # def test_failed_get_request(self, value_mock):
    #     """ Error handlers for failed GET """
    #     value_mock.return_value = 0
    #     value_mock.side_effect = Exception()
    #     resp = self.app.get('/counter')
    #     self.assertEqual(resp.status_code, 500)

    @patch("service.models.Counter.increment")
    def test_failed_post_request(self, value_mock):
        """ Error handlers for failed POST """
        value_mock.return_value = 0
        value_mock.side_effect = Exception()
        resp = self.app.post("/counter")
        self.assertEqual(resp.status_code, 503)

    # @patch("service.models.Counter.value")
    # def test_failed_delete_request(self, value_mock):
    #     """ Error handlers for failed DELETE """
    #     value_mock.return_value = 0
    #     value_mock.side_effect = Exception()
    #     resp = self.app.delete("/counter")
    #     self.assertEqual(resp.status_code, 503)

    # @patch('flask.request.get_json')
    # def test_failed_post_request(self, value_mock):
    #     """ Error handlers for failed PUT """
    #     value_mock.side_effect = Exception()
    #     data = {"counter": 0}
    #     resp = self.app.put('/counter', json=data)
    #     self.assertEqual(resp.status_code, 500)


if __name__ == "__main__":
    unittest.main()
