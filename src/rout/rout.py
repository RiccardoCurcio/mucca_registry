"""Mucca Rout."""
import json
import os
import sys
from src.controller.controller import controller
from vendor.mucca_logging.mucca_logging import logging


class rout():
    """Rout Class."""

    def __init__(self, request):
        """Init."""
        self.servicename = os.getenv("SERVICE_NAME")
        self.serviceversion = os.getenv("VERSION")
        self.request = request
        self.actions = ['read', 'create']
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

    def router(self):
        """Router."""
        if self.__getServiceVersion() == self.serviceversion and self.__getServiceName() == self.servicename:
            if self.__getServiceAction() in self.actions:
                new_controller = controller()
                func = getattr(new_controller, self.__getServiceAction())
                return func(self.__getBody())
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
