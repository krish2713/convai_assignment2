import os

class Config:
    # Database URL (can be sqlite, PostgreSQL, etc.)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///travel.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
