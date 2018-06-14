import sys

from vendor.mucca_connector import mucca_connector
from src.rout.rout import rout

class app():
    def __init__(self, app_name):
        print(app_name)
        pass

    def run(self):
        mucca_connector_server = mucca_connector()
        mucca_connector_server.serverHandler(6001, 1048, registry_routing)

def registry_routing(message):
    print(message)
    new_request = rout(message)
    return new_request.router()

if __name__ == '__main__':
    app = app("Mucca registry")
    app.run()
