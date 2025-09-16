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
    
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    if not GOOGLE_API_KEY:
        logging.error("google api key must be set in .env file")
        raise ValueError("google api key must be set in .env file")
    


