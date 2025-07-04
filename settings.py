import os

from dotenv import load_dotenv

load_dotenv()

MONGO_CV_URI = os.getenv('MONGO_CV_URI') or ''
MONGO_CV_NAME = os.getenv('MONGO_CV_NAME') or ''
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN') or ''
CHAT_IDS = [645403230]
