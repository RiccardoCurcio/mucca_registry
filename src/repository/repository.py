from pymongo import MongoClient
import os

class repository:
    def __init__(self):
        MONGO_CLIENT_ADDR = os.getenv("MONGO_CLIENT")
        CLIENT_DB = os.getenv("CLIENT_DB")
        DB_COLLECTION = os.getenv("DB_COLLECTION")
        self.client = MongoClient(MONGO_CLIENT_ADDR)
        self.db = self.client[CLIENT_DB]
        self.collection = self.db[DB_COLLECTION]
        pass

    def getServicePort(self, version, name):
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
            return None
        found = get_result.distinct("port")
        print(found[0])
        return found[0]

    def createServicePort(self, version, name, port):
        if self.getServicePort(version, name) is not None:
            return False
        add = {"version": version, "serviceName": name,"port": port}
        if self.getServiceByPort(port) is None:
            try:
                result = self.collection.insert_one(add)
                print('CREATING SERVICE PORT (repository) version {} name: {} port {}'.format(version, name, port))
                return True
            except InvalidOperation as emsg:
                print('Invalid operation {}'.format(emsg))
                return "no"
                # err 500?
        return False

    def getServiceByPort(self, port):
        check = {"port": port}
        return self.collection.find_one(check)
