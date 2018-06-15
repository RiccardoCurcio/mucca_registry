from dotenv import load_dotenv
from dotenv import find_dotenv
import os
from vendor.mucca_connector_py.mucca_connector import mucca_connector
from src.rout.rout import rout

class app():
    def __init__(self, app_name):
        load_dotenv(find_dotenv())
        self.port = os.getenv("PORT")
        self.buffersize = os.getenv("BUFFERSIZE")
        print(app_name)
        pass

    def run(self):
        mucca_connector_server = mucca_connector()
        mucca_connector_server.serverHandler(int(self.port), int(self.buffersize), registry_routing)

def registry_routing(message):
    print(message)
    new_request = rout(message)
    return new_request.router()

if __name__ == '__main__':
    app = app("Mucca registry")
    app.run()
