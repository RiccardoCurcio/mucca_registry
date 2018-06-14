from src.repository.repository import repository
import json

class controller():
    def __init__(self):
        pass

    def getServicePort(self, params):
        new_repository = repository()
        data_response = new_repository.getServicePort(params['version'], params['serviceName'])
        status = "200"
        if data_response is None:
            status = "404"
        get_port_response = {"service":{"status": status, "serviceName":"registry","action":"getServicePort"},"head":{},"body":{"port":"not found"}}
        print(json.dumps(get_port_response))
        return json.dumps(get_port_response)

    def createServicePort(self, params):
        new_repository = repository()
        data_response = new_repository.createServicePort(params['version'], params['serviceName'], params['port'])
        status = "201"
        statusMessage = "created"
        if data_response is False:
            status = "409"
            statusMessage = "port already occupied or version/name already exists"
        if data_response is "no":
            status = "500"
            statusMessage = "Database error, invalid operation"
        create_port_response = {"service":{"status":status,"serviceName":"registry","action":"createServicePort"},"head":{},"body":{"statusMessage":statusMessage}}
        print(json.dumps(create_port_response))
        return json.dumps(create_port_response)
