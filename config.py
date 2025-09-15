import os
from dotenv import load_dotenv
import logging

load_dotenv()
class Config:
    #load your database URL
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if not DATABASE_URL:
        logging.error("DATABASE_URL must be set in the .env file")
        raise ValueError("DATABASE_URL must be set in the .env file")
    


