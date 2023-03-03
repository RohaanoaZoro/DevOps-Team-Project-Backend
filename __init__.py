import os
import tempfile
from functools import reduce

from tinydb import TinyDB, Query

import connexion
import six
import json 

from swagger_server.models.student import Student  # noqa: E501
from swagger_server import util
from swagger_server.service.dbconnect import MongoDatabase


db_dir_path = tempfile.gettempdir()
db_file_path = os.path.join(db_dir_path, "students.json")
student_db = TinyDB(db_file_path)

from pymongo import MongoClient
colz = MongoDatabase()

import bson
from bson import ObjectId



def add(student=None):
   
    temp_dict = {"first_name":student.first_name, "last_name": student.last_name}

    res = colz.find_one(temp_dict)
    if res:
        return 'already exists', 409


    colz.insert_one(student.to_dict())

    res = colz.find_one(temp_dict)
    if res:
        return str(res["_id"])
    else: 
        return 'could not add to mongo', 400


def get_by_id(student_id=None, subject=None):

    response = {}
    if bson.objectid.ObjectId.is_valid(student_id):

        temp_dict = {"_id": ObjectId(student_id)}
        res = colz.find_one(temp_dict)
        if res:
            return {
                'student_id': str(res["_id"]),
                'first_name':res['first_name'],
                'last_name': res['last_name'],
                'grade_records': res['grade_records']
            }
        else:
            return 'not found', 404
    else:
        return 'not found', 404


def delete(student_id=None):
    temp_dict = {"_id": ObjectId(student_id)}
    res = colz.find_one(temp_dict)
    if not res:
        return 'not found', 404    
    colz.delete_one(temp_dict)

    res = colz.find_one(temp_dict)
    if not res:
        return str(student_id)
    else: 
        return 'could not add to mongo', 400


