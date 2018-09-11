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
"""Mucca Controller."""
from src.repository.repository import repository
from vendor.mucca_logging.mucca_logging import logging
import json
import os
import sys


class controller():
    """Controller class."""

    def __init__(self, mongo_connection_instance):
        """Init."""
        self.servicename = os.getenv("SERVICE_NAME")
        self.mongo_connection_instance = mongo_connection_instance
        pass

    def read(self, params, query):
        """Read."""
        new_repository = repository(self.mongo_connection_instance)
        data_response_port, data_response_host = new_repository.read(
            params['version'],
            params['serviceName']
        )
        logging.log_info(
            'Controller reading database...',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        status = "200"
        if data_response_port is None:
            status = "404"
            data_response_port = None
            data_response_host = None
            logging.log_warning(
                'Port/host not found',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
        get_port_response = {
            "service": {
                "status": status,
                "serviceName": "registry",
                "action": "read"
                },
            "head": {
                "Content-Type": "application/json;charset=utf-8",
                "Mucca-Service": self.servicename
                },
            "body": {
                "port": data_response_port,
                "host": data_response_host
                }
            }
        logging.log_info(
            json.dumps(get_port_response),
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        return json.dumps(get_port_response)

    def create(self, params, query):
        """Create."""
        try:
            new_repository = repository(self.mongo_connection_instance)
            data_response = new_repository.create(
                params['version'],
                params['serviceName'],
                params['port'],
                params['host']
            )
            logging.log_info(
                'Controller crating...',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
        except KeyError as emsg:
            data_response = None
            error_message = {
                "service": {
                    "status": "400",
                    "serviceName": "registry",
                    "action": "create"
                    },
                "head": {
                    "Content-Type": "application/json;charset=utf-8",
                    "Mucca-Service": self.servicename
                    },
                "body": {
                    "statusMessage": "bad request",
                    "_id": data_response
                    }
                }
            logging.log_warning(
                "bad request {}".format(emsg),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return json.dumps(error_message)
        status = "201"
        statusMessage = "created"
        if data_response is False:
            status = "409"
            statusMessage = "port already occupied or vers/name already exists"
            data_response = None
            logging.log_warning(
                'Port occupied or version/name already exists in db',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
        if data_response is "no":
            status = "500"
            statusMessage = "Database error, invalid operation"
            data_response = None
            logging.log_error(
                'Database error, invalid operation',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
        create_port_response = {
            "service": {
                "status": status,
                "serviceName": "registry",
                "action": "create"
                },
            "head": {
                "Content-Type": "application/json;charset=utf-8",
                "Mucca-Service": self.servicename
                },
            "body": {
                "statusMessage": statusMessage,
                "_id": data_response
                }
            }
        logging.log_info(
            json.dumps(create_port_response),
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        return json.dumps(create_port_response)

    def update(self, params, query):
        """Update."""
        try:
            new_repository = repository(self.mongo_connection_instance)
            data_response = new_repository.update(
                query['_id']
            )
            logging.log_info(
                'Controller Updating...',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
        pass

    def delete(self, params, query):
        """Delete."""
        try:
            new_repository = repository(self.mongo_connection_instance)
            data_response = new_repository.delete(
                query['_id'],
                params['version'],
                params['serviceName'],
                params['port'],
                params['host']
            )
            logging.log_info(
                'Controller Deleting...',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
        pass
