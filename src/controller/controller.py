from src.repository.repository import repository
import json

class controller():
    def __init__(self):
        pass

    def getServicePort(self, params):
        new_repository = repository()
        data_response_port, data_response_host = new_repository.getServicePort(params['version'], params['serviceName'])
        status = "200"
        if data_response_port is None:
            status = "404"
            data_response_port = None
            data_response_host = None
        get_port_response = {"service":{"status": status, "serviceName":"registry","action":"getServicePort"},"head":{},"body":{"port":data_response_port,"host":data_response_host}}
        print(json.dumps(get_port_response))
        return json.dumps(get_port_response)

    def createServicePort(self, params):
        new_repository = repository()
        data_response = new_repository.createServicePort(params['version'], params['serviceName'], params['port'], params['host'])
        status = "201"
        statusMessage = "created"
        if data_response is False:
            status = "409"
            statusMessage = "port already occupied or version/name already exists"
            data_response = None
        if data_response is "no":
            status = "500"
            statusMessage = "Database error, invalid operation"
            data_response = None
        create_port_response = {"service":{"status":status,"serviceName":"registry","action":"createServicePort"},"head":{},"body":{"statusMessage":statusMessage,"_id":data_response}}
        print(json.dumps(create_port_response))
        return json.dumps(create_port_response)
