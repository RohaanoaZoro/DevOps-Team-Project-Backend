
from pymongo import MongoClient

def MongoDatabaseProperty():
    # client = MongoClient('localhost', 27017,  username='Roal5809', password='Zxcvbnm@2')
    client = MongoClient('localhost', 27017)
    db = client.Devops_db
    colz = db.property
    return colz