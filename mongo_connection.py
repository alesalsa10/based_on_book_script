""" database connection """
import os
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

mongoURI = os.getenv('mongoURI')
cluster = MongoClient(mongoURI)

def mongodb_conn():
    """ connection to mongodb """
    try:
        print('Connection success')
        return MongoClient(mongoURI)
    except pymongo.errors.ConnectionFailure():
        print('Could not connect to server')
