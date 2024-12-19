import os
from dotenv import load_dotenv

load_dotenv()

# Отримуємо URL бази даних
database_url = os.getenv('DATABASE_URL')
if not database_url:
    raise ValueError("DATABASE_URL не знайдено в змінних середовища")

class Config:
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')