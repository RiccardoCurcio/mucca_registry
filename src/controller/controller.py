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
        response_port, response_host, response_id, response_flag = new_repository.read(
            params['version'],
            params['serviceName']
        )
        logging.log_info(
            'Controller reading database...',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        status = "200"
        if response_port is None:
            status = "404"
            response_port = None
            response_host = None
            response_id = None
            response_flag = None
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
                "port": response_port,
                "host": response_host,
                "response_flag": response_flag,
                "_id": str(response_id)
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
            port = None
            flag = 1
            if 'port' in params:
                port = params['port']
            if 'response_flag' in params:
                flag = params['response_flag']
            data_response, selected_port, resp_flag = new_repository.create(
                params['version'],
                params['serviceName'],
                params['host'],
                port,
                flag
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
            selected_port = None
            resp_flag = None
            logging.log_warning(
                'Port occupied or version/name already exists in db',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
        if data_response is "no":
            status = "500"
            statusMessage = "Database error, invalid operation"
            data_response = None
            selected_port = None
            resp_flag = None
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
                "_id": data_response,
                "port": selected_port,
                "response_flag": resp_flag
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
            query_id = None
            version = None
            serviceName = None
            port = None
            host = None
            flag = None
            if '_id' in query:
                query_id = query['_id']
            if 'version' in params:
                version = params['version']
            if 'serviceName' in params:
                serviceName = params['serviceName']
            if 'port' in params:
                port = params['port']
            if 'host' in params:
                host = params['host']
            if 'response_flag' in params:
                flag = params['response_flag']
            data_response = new_repository.update(
                query_id,
                version,
                serviceName,
                port,
                host,
                flag
            )
            logging.log_info(
                'Controller Updating...',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            status = "201"
            statusMessage = "Updated"
        except Exception as emsg:
            logging.log_error(
                'Controller Update error {}'.format(emsg),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            status = "500"
            statusMessage = "Update Controller Error"
        if data_response is None:
            status = "500"
            statusMessage = "Update Operation Fail"
        update_response = {
            "service": {
                "status": status,
                "serviceName": "registry",
                "action": "update"
                },
            "head": {
                "Content-Type": "application/json;charset=utf-8",
                "Mucca-Service": self.servicename
                },
            "body": data_response
            }
        logging.log_info(
            json.dumps(update_response),
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        return json.dumps(update_response)

    def delete(self, params, query):
        """Delete."""
        try:
            new_repository = repository(self.mongo_connection_instance)
            query_id = None
            if '_id' in query:
                query_id = query['_id']
            data_response = new_repository.delete(
                query_id
            )
            status = "200"
            statusMessage = "Deleted"
        except Exception as emsg:
            logging.log_error(
                'Controller Delete error {}'.format(emsg),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            status = "500"
            statusMessage = "Delete Controller error"
        if data_response is None:
            logging.log_warning(
                'No Service Deleted',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            status = "500"
            statusMessage = "No Service Deleted"
        delete_response = {
            "service": {
                "status": status,
                "serviceName": "registry",
                "action": "delete"
                },
            "head": {
                "Content-Type": "application/json;charset=utf-8",
                "Mucca-Service": self.servicename
                },
            "body": {
                "statusMessage": statusMessage,
                "_id": query_id,
                "response": data_response
                }
            }
        return json.dumps(delete_response)

    def readAll(self, params, query):
        """Read full db."""
        try:
            new_repository = repository(self.mongo_connection_instance)
            data_response = new_repository.readAll()
            status = "200"
            logging.log_info(
                'Controller getting full services/port list...',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
        except Exception as emsg:
            logging.log_error(
                'Controller readAll error {}'.format(emsg),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            status = "500"
        full_read_response = {
            "service": {
                "status": status,
                "serviceName": "registry",
                "action": "readAll"
                },
            "head": {
                "Content-Type": "application/json;charset=utf-8",
                "Mucca-Service": self.servicename
                },
            "body": {
                }
            }
        if data_response is None:
            status = "500"
            return json.dumps(full_read_response)
        full_read_response['body'].update(data_response)
        logging.log_info(
            'Controller sending full list: {}'.format(full_read_response),
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        return json.dumps(full_read_response)
