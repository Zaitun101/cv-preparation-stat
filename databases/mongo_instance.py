from pymongo import MongoClient
from settings import MONGO_CV_URI, MONGO_CV_NAME
import certifi

ca = certifi.where()


class MongoInstance:
    def __init__(self, client: str = MONGO_CV_URI):
        self.client = MongoClient(
            client + '/connectTimeoutMS=10000',
            minPoolSize=1,
            maxPoolSize=1,
            TLSCAFile=ca,
        )

    def get_db(self):
        return self.client.get_database(MONGO_CV_NAME)
