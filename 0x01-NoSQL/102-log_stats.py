"""  a Python function that returns the list
of school having a specific topic """
from pymongo import MongoClient


def schools_by_topic(mongo_collection, topic):
    """ Searches for documents that have the given "topic"
 in their topics filed

 Args:
     mongo_collection (Collection): pymongo collection object
     topic (string): Topic to look for in topics field

 Returns:
     List: A list of school names having the specific topic
 """
    result = mongo_collection.find({"topics": {"$in": [topic]}})
    return [documents["name"] for documents in result]
