from src.repository.repository import repository
import json
import os

class controller():
    def __init__(self):
        self.servicename = os.getenv("SERVICE_NAME")
        pass

    def read(self, params):
        new_repository = repository()
        data_response_port, data_response_host = new_repository.read(params['version'], params['serviceName'])
        status = "200"
        if data_response_port is None:
            status = "404"
            data_response_port = None
            data_response_host = None
        get_port_response = {"service":{"status": status, "serviceName":"registry","action":"read"},"head":{"Content-Type":"application/json;charset=utf-8","Mucca-Service":self.servicename},"body":{"port":data_response_port,"host":data_response_host}}
        print(json.dumps(get_port_response))
        return json.dumps(get_port_response)

    def create(self, params):
        try:
            new_repository = repository()
            data_response = new_repository.create(params['version'], params['serviceName'], params['port'], params['host'])
        except KeyError as emsg:
            data_response = None
            error_message = {"service":{"status":"400","serviceName":"registry","action":"create"},"head":{"Content-Type":"application/json;charset=utf-8","Mucca-Service":self.servicename},"body":{"statusMessage":"bad request","_id":data_response}}
            print("bad request {}".format(emsg))
            return json.dumps(error_message)
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
        create_port_response = {"service":{"status":status,"serviceName":"registry","action":"create"},"head":{"Content-Type":"application/json;charset=utf-8","Mucca-Service":self.servicename},"body":{"statusMessage":statusMessage,"_id":data_response}}
        print(json.dumps(create_port_response))
        return json.dumps(create_port_response)
