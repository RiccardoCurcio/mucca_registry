"""Mucca Repository."""
from pymongo import MongoClient
import os
import sys
from vendor.mucca_logging.mucca_logging import logging
from src.mongo_connection.mongo_connection import mongo_connection


class repository:
    """Repository class."""

    def __init__(self, connection):
        """Init."""
        self.mongo_client_addr = os.getenv("MONGO_CLIENT")
        self.client_db = os.getenv("CLIENT_DB")
        self.db_collection = os.getenv("DB_COLLECTION")
        self.client = MongoClient(self.mongo_client_addr)
        self.db = self.client[self.client_db]
        self.collection = self.db[self.db_collection]
        self.connection_data = connection
        self.coll_conn = connection["collection"]
        pass

    def read(self, version, name):
        """Read."""
        # data = mongo_connection.create_connection()
        # print(data)
        # conn = data["collection"]
        find = {"version": version, "serviceName": name}
        try:
            # get_result = self.collection.find(find)
            get_result = self.coll_.find(find)
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
            return None, None
        port_found = get_result.distinct("port")
        host_found = get_result.distinct("host")
        logging.log_info(
            'Repository found service on port: {} host: {}'.format(
                port_found[0],
                host_found[0]
            ),
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        return port_found[0], host_found[0]

    def create(self, version, name, port, host):
        """Create."""
        logging.log_info(
            'Repository verifying request...',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        port_check, host_check = self.read(version, name)
        if port_check is not None:
            return False
        add = {
            "version": version,
            "serviceName": name,
            "port": port,
            "host": host
            }
        if self.getServiceByPort(port) is None:
            try:
                result = self.collection.insert_one(add).inserted_id
                logging.log_info(
                    'Repository creating service port for version {} name: {} port {} host {}'.format(
                        version,
                        name,
                        port,
                        host
                    ),
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                )
                return str(result)
            except InvalidOperation as emsg:
                logging.log_error(
                    'Invalid operation: {}'.format(emsg),
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                )
                return "no"
        return False

    def getServiceByPort(self, port):
        """GetServiceByPort."""
        logging.log_info(
            'Checking if requested port is free...',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        check = {"port": port}
        return self.collection.find_one(check)

    def dbCheck(self):
        """DbCheck."""
        db_names = self.client.database_names()
        if self.client_db not in db_names:
            return False
        return True
