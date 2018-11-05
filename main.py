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
"""Mucca Registry."""
from dotenv import load_dotenv
from dotenv import find_dotenv
import os
import sys
from vendor.mucca_connector_py.mucca_connector import mucca_connector
from vendor.mucca_logging.mucca_logging import logging
from src.mongo_connection.mongo_connection import mongo_connection
from src.rout.rout import rout
from src.boot.boot import boot


class app():
    """Class app."""

    def __init__(self, app_name):
        """Class constructor."""
        self.port = os.getenv("PORT")
        self.buffersize = os.getenv("BUFFERSIZE")
        logging.log_info(
            app_name,
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        pass

    def run(self):
        """Run app."""
        boot.init()
        mucca_connector_server = mucca_connector()
        mucca_connector_server.serverHandler(
            int(self.port),
            int(self.buffersize),
            registry_routing
        )


def registry_routing(message):
    """Registry routing."""
    logging.log_info(
        message,
        os.path.abspath(__file__),
        sys._getframe().f_lineno
    )
    new_request = rout(message, mongo_connection_instance)
    return new_request.router()


if __name__ == '__main__':
    try:
        load_dotenv(find_dotenv())
        service_name = os.getenv("SERVICE_NAME")
        client_address = os.getenv("MONGO_CLIENT")
        mongo_connection_instance = mongo_connection(client_address)
        app = app(service_name)
        app.run()
    except KeyboardInterrupt:
        logging.log_info(
            "Intercepted KeyboardInterrupt close {}".format(service_name),
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        del app
        sys.exit()
