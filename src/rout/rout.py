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
"""Mucca Rout."""
import json
import os
import sys
from src.controller.controller import controller
from vendor.mucca_logging.mucca_logging import logging


class rout():
    """Rout Class."""

    def __init__(self, request, mongo_connection_instance):
        """Init."""
        self.servicename = os.getenv("SERVICE_NAME")
        self.serviceversion = os.getenv("VERSION")
        self.request = request
        self.actions = ['read', 'create', 'update', 'delete']
        self.mongo_connection_instance = mongo_connection_instance
        pass

    def __getServiceVersion(self):
        try:
            return json.loads(self.request.decode())["service"]["version"]
        except json.decoder.JSONDecodeError as emsg:
            logging.log_error(
                emsg,
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None
        except KeyError as emsg:
            logging.log_error(
                emsg,
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None

    def __getServiceName(self):
        try:
            return json.loads(self.request.decode())["service"]["serviceName"]
        except json.decoder.JSONDecodeError as emsg:
            logging.log_error(
                emsg,
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None
        except KeyError as emsg:
            logging.log_error(
                emsg,
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None

    def __getServiceAction(self):
        try:
            return json.loads(self.request.decode())["service"]["action"]
        except json.decoder.JSONDecodeError as emsg:
            logging.log_error(
                emsg,
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None
        except KeyError as emsg:
            logging.log_error(
                emsg,
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None

    def __getBody(self):
        try:
            return json.loads(self.request.decode())["body"]
        except json.decoder.JSONDecodeError as emsg:
            logging.log_error(
                emsg,
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None
        except KeyError as emsg:
            logging.log_error(
                emsg,
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None

    def __getQuery(self):
        try:
            return json.loads(self.request.decode())["query"]
        except json.decoder.JSONDecodeError as emsg:
            logging.log_error(
                emsg,
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None
        except KeyError as emsg:
            logging.log_error(
                emsg,
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None

    def router(self):
        """Router."""
        if self.__getServiceVersion() == self.serviceversion and self.__getServiceName() == self.servicename:
            if self.__getServiceAction() in self.actions:
                new_controller = controller(self.mongo_connection_instance)
                func = getattr(new_controller, self.__getServiceAction())
                return func(self.__getBody(), self.__getQuery())
            else:
                logging.log_warning(
                    'Bad request',
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                )
                error_msg = {
                    "service": {
                        "status": "400",
                        "serviceName": "registry",
                        "action": self.__getServiceAction()
                        },
                    "head": {
                        "Content-Type": "application/json;charset=utf-8",
                        "Mucca-Service": self.servicename
                        },
                    "body": {
                        "statusMessage": "bad request"
                        }
                    }
                return json.dumps(error_msg)
        logging.log_warning(
            'Bad request',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        error_msg = {
            "service": {
                "status": "400",
                "serviceName": "registry",
                "action": self.__getServiceAction()
                },
            "head": {
                "Content-Type": "application/json;charset=utf-8",
                "Mucca-Service": self.servicename
                },
            "body": {
                "statusMessage": "bad request"
                }
            }
        return json.dumps(error_msg)
