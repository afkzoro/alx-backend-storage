#!/usr/bin/env python3
""" a Python function that lists all documents in a collection """
from pymongo import MongoClient


def list_all(mongo_collection):
    """_summary_

 Args:
     mongo_collection (Collection): pymongo collection object

 Returns:
     list:  an empty list if no document in the collection
 """
    cursorObj = mongo_collection.find()
    documents = list(cursorObj)
    return documents
