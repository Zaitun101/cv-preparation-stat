from databases.mongo_instance import MongoInstance
from datetime import datetime, timedelta


class Mongo:
    def __init__(self):
        mongo_instance = MongoInstance()
        self.collection = mongo_instance.get_db()['bot_analytics']

    def find_documents(self, filters: dict, projection: dict = None) -> list:
        """Возвращает все документы по фильтру в виде списка"""
        cursor = self.collection.find(filters, projection)
        return list(cursor)

    def get_events(self, hours: int) -> list:
        """Получает все события за последние `hours` часов"""
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)

        query = {
            'timestamp': {'$gte': start_time, '$lte': end_time},
        }

        projection = {
            '_id': 0,
            'group_id': 0,
            'duration': 0,
            'finish_time': 0,
            'start_time': 0,
        }

        return self.find_documents(query, projection)
