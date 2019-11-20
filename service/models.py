######################################################################
# Copyright 2016, 2017 John Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################
"""
Counter Model
"""
import os
import re
import logging
from redis import Redis
from redis.exceptions import ConnectionError

logger = logging.getLogger(__name__)


class DatabaseConnectionError(ConnectionError):
    pass


class Counter(object):
    """ An integer counter that is persisted in Redis

    You can establish a connection to Redis using an environment
    variable DATABASE_URI in the following format:

        DATABASE_URI="redis://userid:password@localhost:6379/0"

    This follows the same standards as SQLAlchemy URIs
    """

    redis = None
    credentials = dict(prefix="", userid="", password="", host="", port=0, database="")

    def __init__(self, name="hits"):
        """ Constructor """
        self.name = name

    @property
    def value(self):
        """ Returns the current value of the counter """
        return int(Counter.redis.get(self.name))

    @value.setter
    def value(self, value):
        """ Sets the value of the counter """
        Counter.redis.set(self.name, value)

    @value.deleter
    def value(self):
        """ Sets the value of the counter to zero (0) """
        Counter.redis.set(self.name, 0)

    def increment(self):
        """ Increments the current value of the counter by 1 """
        return Counter.redis.incr(self.name)

    ######################################################################
    #  R E D I S   D A T A B A S E   C O N N E C T I O N   M E T H O D S
    ######################################################################

    @classmethod
    def reset_credentials(cls):
        """ Re-initializes the credentials """
        cls.credentials = dict(
            prefix="", userid="", password="", host="", port=0, database=""
        )

    @classmethod
    def parse_uri(cls, database_uri):
        """ Parses a database uri into it's credentials

        Parameter Format:
            "redis://userid:password@localhost:6379/0"

        """
        try:
            uri_regex = r"^(.*:)\/\/(.*):(.*)@([A-Za-z0-9\-\.]+):([0-9]+)\/(.*)$"
            tokens = re.search(uri_regex, database_uri)
            cls.credentials["prefix"] = tokens.group(1)
            cls.credentials["userid"] = tokens.group(2)
            cls.credentials["password"] = tokens.group(3)
            cls.credentials["host"] = tokens.group(4)
            cls.credentials["port"] = int(tokens.group(5))
            cls.credentials["database"] = tokens.group(6)
        except AttributeError as err:
            msg = "DATABASE URI could not be parsed: {}".format(str(err))
            logger.error(msg)
            raise DatabaseConnectionError(msg)

    @classmethod
    def test_connecion(cls):
        """ Test connection by pinging the host """
        success = False
        try:
            cls.redis.ping()
            logger.info("Connection established")
            success = True
        except ConnectionError:
            logger.warning("Connection Error!")
        return success

    @classmethod
    def connect(cls, database_uri=None):
        """ Established database connection

        Arguments:
            database_uri: a uri to the Redis database

        Raises:
            DatabaseConnectionError: Could not connect
        """
        if database_uri:
            cls.parse_uri(database_uri)
        elif "DATABASE_URI" in os.environ:
            DATABASE_URI = os.environ["DATABASE_URI"]
            cls.parse_uri(DATABASE_URI)
        else:
            msg = "Missing Credentials"
            logger.error(msg)
            raise DatabaseConnectionError(msg)

        logger.info(
            "Attempting to connecting to Redis at: %s:%s",
            cls.credentials["host"],
            cls.credentials["port"],
        )

        cls.redis = Redis(
            host=cls.credentials["host"],
            port=cls.credentials["port"],
            password=cls.credentials["password"],
            charset="utf-8",
            decode_responses=True,
        )

        if not cls.test_connecion():
            # if you end up here, redis instance is down.
            cls.redis = None
            logger.fatal("*** FATAL ERROR: Could not connect to the Redis Service")
            raise DatabaseConnectionError("Could not connect to the Redis Service")

        logger.info(
            'Successfully connected to Redis on %s:%s',
            cls.credentials["host"],
            cls.credentials["port"],
        )
        return cls.redis
