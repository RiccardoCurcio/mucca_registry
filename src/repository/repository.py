from pymongo import MongoClient
import os

class repository:
    def __init__(self):
        self.mongo_client_addr = os.getenv("MONGO_CLIENT")
        self.client_db = os.getenv("CLIENT_DB")
        self.db_collection = os.getenv("DB_COLLECTION")
        self.client = MongoClient(self.mongo_client_addr)
        self.db = self.client[self.client_db]
        self.collection = self.db[self.db_collection]
        pass

    def read(self, version, name):
        find = {"version":version,"serviceName":name}
        try:
            get_result = self.collection.find(find)
            print('Getting service port (repository) for: name {} version {}'.format(name, version))
        except TypeError as emsg:
            print('Type argument error{}'.format(emsg))
        try:
            count = get_result.count()
        except OperationFailure as emsg:
            print('Database error: {}'.format(emsg))
        if count is 0:
            print('No match found')
            return None, None
        port_found = get_result.distinct("port")
        host_found = get_result.distinct("host")
        print(port_found[0],host_found[0])
        return port_found[0],host_found[0]

    def create(self, version, name, port, host):
        port_check, host_check = self.read(version, name)
        if port_check is not None:
            return False
        add = {"version": version, "serviceName": name,"port": port, "host": host}
        if self.getServiceByPort(port) is None:
            try:
                result = self.collection.insert_one(add).inserted_id
                print('CREATING SERVICE PORT (repository) version {} name: {} port {} host {}'.format(version, name, port, host))
                return str(result)
            except InvalidOperation as emsg:
                print('Invalid operation {}'.format(emsg))
                return "no"
        return False

    def getServiceByPort(self, port):
        check = {"port": port}
        return self.collection.find_one(check)

    def dbCheck(self):
        db_names = self.client.database_names()
        if self.client_db not in db_names:
            return False
        return True
