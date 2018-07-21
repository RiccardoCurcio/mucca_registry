"""Mucca Controller."""
from src.repository.repository import repository
from vendor.mucca_logging.mucca_logging import logging
import json
import os
import sys


class controller():
    """Controller class."""

    def __init__(self):
        """Init."""
        self.servicename = os.getenv("SERVICE_NAME")
        pass

    def read(self, params):
        """Read."""
        new_repository = repository()
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

    def create(self, params):
        """Create."""
        try:
            new_repository = repository()
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
                'Port occupied or v/name already exists in db',
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
