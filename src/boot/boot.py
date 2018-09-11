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
"""Mucca Boot."""
import os
import sys
from src.repository.repository import repository
from vendor.mucca_logging.mucca_logging import logging
from src.mongo_connection.mongo_connection import mongo_connection


class boot:
    """Boot Class."""

    @staticmethod
    def init():
        """Init."""
        client_address = os.getenv("MONGO_CLIENT")
        mongo_connection_instance = mongo_connection(client_address)
        boot_repo = repository(mongo_connection_instance)
        if boot_repo.dbCheck() is False:
            logging.log_info(
                'Creating database',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            boot.insertMyself(boot_repo)
            boot.insertCrudGenerator(boot_repo)
        logging.log_info(
            'Repository booted',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        mongo_connection_instance.closeConnection()
        del boot_repo
        return True

    @staticmethod
    def insertMyself(repo_instance):
        """InsertMyself."""
        version = os.getenv("VERSION")
        name = os.getenv("SERVICE_NAME")
        port = os.getenv("PORT")
        host = os.getenv("HOST")
        logging.log_info(
            'Inserting myself...',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        repo_instance.create(version, name, port, host)
        return None

    @staticmethod
    def insertCrudGenerator(repo_instance):
        """insertCrudGenerator."""
        version = os.getenv("CRUD_GENERATOR_VERSION")
        name = os.getenv("CRUD_GENERATOR_NAME")
        port = os.getenv("CRUD_GENERATOR_PORT")
        host = os.getenv("CRUD_GENERATOR_HOST")
        logging.log_info(
            'Inserting Crud Generator...',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        repo_instance.create(version, name, port, host)
        return None
