# Copyright 2018 Federica Cricchio
# fefender@gmail.com
#
# This file is part of mucca_registry.
#
# mucca_registry is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mucca_registry is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with mucca_registry.  If not, see <http://www.gnu.org/licenses/>.
"""Mongo Connection."""
from pymongo import MongoClient
import os
import sys
from vendor.mucca_logging.mucca_logging import logging
from pymongo.errors import ConnectionFailure


class mongo_connection():
    """Connection."""

    def __init__(self, client_address):
        """Init Mongo Connection."""
        self.__mongo_client_address = client_address
        self.__client = None
        self.__connection_counter = 0

    def setConnection(self):
        """Set Connection to Mongo."""
        if self.__client is None:
            logging.log_info(
                'Connecting to MongoClient...',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )
            try:
                self.__client = MongoClient(self.__mongo_client_address)
                self.__client.server_info()
                self.__connection_counter = 0
                logging.log_info(
                    'Succesfully connected to MongoClient',
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                    )
            except ConnectionFailure as emsg:
                logging.log_error(
                    'Connection to MongoClient failed: {}'.format(emsg),
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                    )
                self.__attemptCounter()
        else:
            try:
                self.__client.server_info()
                self.__connection_counter = 0
                logging.log_info(
                    'Connection to MongoClient still alive',
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                    )
            except ConnectionFailure as emsg:
                logging.log_error(
                    'Connection to MongoClient fail: {}'.format(emsg),
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                    )
                self.__attemptCounter()

    def getConnection(self):
        """Get Mongo connection client."""
        if(self.__client is None):
            self.setConnection()
        return self.__client

    def closeConnection(self):
        """Close Mongo Client."""
        try:
            self.__client.close()
            self.__client = None
        except Exception as emsg:
            logging.log_error(
                'Connection closing fail: {}'.format(emsg),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )

    def __attemptCounter(self):
        self.__connection_counter += 1
        if self.__connection_counter <= 3:
            logging.log_info(
                'MongoClient connection attempt n°{}. Connecting...'.format(
                    self.__connection_counter),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )
            self.setConnection()
        else:
            logging.log_error(
                'Mongo Connection refused. Exiting',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )
            sys.exit(1)
