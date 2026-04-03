import os

class Config:
    SECRET_KEY = 'mysecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///notes.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
