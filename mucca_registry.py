from dotenv import load_dotenv
from dotenv import find_dotenv
import os, sys
from vendor.mucca_connector_py.mucca_connector import mucca_connector
from vendor.mucca_logging.mucca_logging import logging
from src.rout.rout import rout
from src.boot.boot import boot

# logging.log_info("info test", os.path.abspath(__file__), sys._getframe().f_lineno)
class app():
    def __init__(self, app_name):
        self.port = os.getenv("PORT")
        self.buffersize = os.getenv("BUFFERSIZE")
        logging.log_info(app_name, os.path.abspath(__file__), sys._getframe().f_lineno)
        pass

    def run(self):
        boot.init()
        mucca_connector_server = mucca_connector()
        mucca_connector_server.serverHandler(int(self.port), int(self.buffersize), registry_routing)

def registry_routing(message):
    logging.log_info(message, os.path.abspath(__file__), sys._getframe().f_lineno)
    new_request = rout(message)
    return new_request.router()

if __name__ == '__main__':
    try:
        load_dotenv(find_dotenv())
        service_name = os.getenv("SERVICE_NAME")
        app = app(service_name)
        app.run()
    except KeyboardInterrupt:
        logging.log_info(
            "Intercepted KeyboardInterrupt close {}".format(service_name),
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        del app
        sys.exit()
