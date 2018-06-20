"""Mucca Boot."""
import os
import sys
from src.repository.repository import repository
from vendor.mucca_logging.mucca_logging import logging


class boot:
    """Boot Class."""

    @staticmethod
    def init():
        """Init."""
        boot_repo = repository()
        if boot_repo.dbCheck() is False:
            logging.log_info(
                'Creating database',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            print("creating db")
            version = os.getenv("VERSION")
            name = os.getenv("SERVICE_NAME")
            port = os.getenv("PORT")
            host = os.getenv("HOST")
            boot_repo.create(version, name, port, host)
        logging.log_info(
            'Repository booted',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        del boot_repo
        return True
