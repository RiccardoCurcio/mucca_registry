from pymongo import MongoClient
import os
from src.repository.repository import repository

class boot:
    @staticmethod
    def init():
        boot_repo = repository()
        print("boot_repo ok")
        if boot_repo.dbCheck() is False:
            print("creating db")
            version = os.getenv("VERSION")
            name = os.getenv("SERVICE_NAME")
            port = os.getenv("PORT")
            host = os.getenv("HOST")
            boot_repo.create(version, name, port, host)
        del boot_repo
        return True
