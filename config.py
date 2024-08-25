import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # Use the DATABASE_URL from the .env file
    SQLALCHEMY_TRACK_MODIFICATIONS = False