"""  a Python function that changes all topics of
 a school document based on the name """
from pymongo import MongoClient


def update_topics(mongo_collection, name, topics):
    """_summary_

 Args:
     mongo_collection (_type_): _description_
     name (_type_): _description_
     topics (_type_): _description_

 Returns:
     _type_: _description_
 """
    # Updates all topics of a school document based on the name
    result = mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
    # Return the number of documents updated
    return result.modified_count
