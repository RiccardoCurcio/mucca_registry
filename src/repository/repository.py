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
"""Mucca Repository."""
from pymongo import MongoClient
import os
import sys
import datetime
from vendor.mucca_logging.mucca_logging import logging
from src.mongo_connection.mongo_connection import mongo_connection
from bson.objectid import ObjectId


class repository:
    """Repository class."""

    def __init__(self, connection_instance):
        """Init."""
        self.port_limit_top = os.getenv("PORT_LIMIT_TOP")
        self.port_limit_bottom = os.getenv("PORT_LIMIT_BOTTOM")
        self.client_db = os.getenv("CLIENT_DB")
        self.db_collection = os.getenv("DB_COLLECTION")
        self.__mongo_instance = connection_instance
        self.__mongo_instance.setConnection()
        self.client = self.__mongo_instance.getConnection()
        self.db = self.client[self.client_db]
        self.collection = self.db[self.db_collection]
        pass

    def read(self, version, name):
        """Read."""
        find = {"version": version, "serviceName": name}
        try:
            get_result = self.collection.find(find)
            logging.log_info(
                'Repository looking for: name {} version {}'.format(
                    name,
                    version
                ),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
        except TypeError as emsg:
            logging.log_error(
                'Type argument error {}'.format(emsg),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
        try:
            count = get_result.count()
        except OperationFailure as emsg:
            logging.log_error(
                'Database error: {}'.format(emsg),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
        if count is 0:
            logging.log_info(
                'No match found',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None, None, None, None
        port_found = get_result.distinct("port")
        host_found = get_result.distinct("host")
        id_found = get_result.distinct("_id")
        flag_found = get_result.distinct("response_flag")
        logging.log_info(
            'Repository found service on port: {} host: {} flag: {}'.format(
                port_found[0],
                host_found[0],
                flag_found[0]
            ),
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        return port_found[0], host_found[0], id_found[0], flag_found[0]

    def readAll(self):
        """Read full db."""
        try:
            get_list = list(self.collection.find())
            logging.log_info(
                'Getting full collection',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return self.__formatResponse(get_list)
        except Exception as emsg:
            logging.log_error(
                'readAll repository fail, exception raised {}'.format(emsg),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None

    def create(self, version, name, host, port, flag):
        """Create."""
        logging.log_info(
            'Repository verifying request...',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        port_check, host_check, id_check, flag_check = self.read(version, name)
        if port_check is not None:
            return False, False, False
        if port is None:
            port = self.__findFreePort()
        created_at = datetime.datetime.utcnow()
        updated_at = None
        deleted_at = None
        response_flag = flag
        add = {
            "version": version,
            "serviceName": name,
            "port": port,
            "host": host,
            "created_at": str(created_at),
            "updated_at": updated_at,
            "deleted_at": deleted_at,
            "response_flag": response_flag
            }
        if self.__getServiceByPort(port) is None:
            try:
                result = self.collection.insert_one(add).inserted_id
                logging.log_info(
                    'Repository creating service port for version {} name: {} port {} host {} flag {}'.format(
                        version,
                        name,
                        port,
                        host,
                        flag
                    ),
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                )
                return str(result), port, response_flag
            except InvalidOperation as emsg:
                logging.log_error(
                    'Invalid operation: {}'.format(emsg),
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                )
                err_one = "no"
                err_two = "no"
                err_three = "no"
                return err_one, err_two, err_three
        return False, False, False

    def update(self, service_id, version, name, port, host, flag):
        """Update."""
        logging.log_info(
            'Updating service...',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        if service_id is None:
            logging.log_warning(
                'Bad request, missing _id',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None
        filter = {"_id": ObjectId(service_id)}
        request = self.__updateRequestFormatter(version, name, port, host, flag)
        update = {"$set": request}
        try:
            result = self.collection.update_one(filter, update)
            full_data = self.__readById(service_id)
            return self.__objIdtoString(full_data)
        except Exception as emsg:
            logging.log_error(
                'Updating fail. Bad request {}'.format(emsg),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None

    def delete(self, service_id):
        """Delete."""
        logging.log_info(
            'Deleting service id: {}'.format(service_id),
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        if service_id is None:
            logging.log_warning(
                'Deleting fail, missing id',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None
        filter = {"_id": ObjectId(service_id)}
        try:
            result = self.collection.delete_one(filter)
        except Exception as emsg:
            logging.log_error(
                'Deleting fail, exception raised {}'.format(emsg),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None
        if result.deleted_count == 0:
            logging.log_warning(
                'Deleting fail, no service deleted. Deleted_count: 0',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None
        logging.log_info(
            'Service Deleted.',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        return str(result)

    def dbCheck(self):
        """DbCheck."""
        db_names = self.client.list_database_names()
        if self.client_db not in db_names:
            return False
        return True

    def collectionCheck(self):
        """Check if Collection Exists."""
        collection_names = self.client.list_database_names()
        logging.log_info(
            'Checking if Collection exists...',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        if self.db_collection not in collection_names:
            return False
        return True

    def __findFreePort(self):
        """Find a free Port in a range."""
        logging.log_info(
            'Searching free port',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        # top_limit = self.port_limit_top
        # bottom_limit = self.port_limit_bottom
        for n in range(int(self.port_limit_top), int(self.port_limit_bottom)):
            port = str(n)
            # port = n
            find_port = {"port": port}
            data = self.collection.find(find_port).count()
            if data is 0:
                logging.log_info(
                    'Free Port Found at: {}'.format(port),
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                )
                return port
        return None

    def __getServiceByPort(self, port):
        """Get Service info By Port."""
        logging.log_info(
            'Checking if requested port is free...',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        check = {"port": port}
        return self.collection.find_one(check)

    def __readById(self, service_id):
        """Read db by id."""
        try:
            search_id = {"_id": ObjectId(service_id)}
            full_data = dict(self.collection.find_one(search_id))
            logging.log_info(
                'Getting service data by id',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return full_data
        except Exception as emsg:
            logging.log_error(
                'readById repository fail, exception raised {}'.format(emsg),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None
        pass

    def __formatResponse(self, list):
        """Stringfy idObject and set Database Response."""
        response = dict()
        if list is None:
            return response
        for x in list:
            list_element = dict(x)
            obj_id = list_element['_id']
            str_id = str(obj_id)
            list_element.update(_id=str_id)
            list_to_dict = dict({str_id: list_element})
            response.update(list_to_dict)
        return response

    def __objIdtoString(self, lista):
        """Format update response."""
        obj_id = lista['_id']
        str_id = str(obj_id)
        lista.update(_id=str_id)
        return lista

    def __updateRequestFormatter(self, version, name, port, host, flag):
        request = dict()
        if version is not None:
            version_ltd = dict({"version": version})
            request.update(version_ltd)
        if name is not None:
            name_ltd = dict({"serviceName": name})
            request.update(name_ltd)
        if port is not None:
            port_ltd = dict({"port": port})
            request.update(port_ltd)
        if host is not None:
            host_ltd = dict({"host": host})
            request.update(host_ltd)
        if flag is not None:
            flag_ltd = dict({"response_flag": flag})
            request.update(flag_ltd)
        updated_at = datetime.datetime.utcnow()
        updater_ltd = dict({"updated_at": str(updated_at)})
        request.update(updater_ltd)
        return request
