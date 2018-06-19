import sys
import json
import os
from src.controller.controller import controller

class rout():
    def __init__(self, request):
        self.servicename = os.getenv("SERVICE_NAME")
        self.request = request
        self.actions = ['read', 'create']
        pass

    def __getServiceVersion(self):
        return json.loads(self.request.decode())["service"]["version"]

    def __getServiceName(self):
        return json.loads(self.request.decode())["service"]["serviceName"]

    def __getServiceAction(self):
        return json.loads(self.request.decode())["service"]["action"]

    def __getBody(self):
        return json.loads(self.request.decode())["body"]

    def router(self):
        if self.__getServiceVersion() == 'v1' and self.__getServiceName() == 'registry':
            if self.__getServiceAction() in self.actions:
                new_controller = controller()
                func = getattr(new_controller, self.__getServiceAction())
                return func(self.__getBody())
            else:
                error_msg = {"service":{"status":"400","serviceName":"registry","action":self.__getServiceAction()},"head":{"Content-Type":"application/json;charset=utf-8","Mucca-Service":self.servicename},"body":{"statusMessage":"bad request"}}
                return json.dumps(error_msg)
