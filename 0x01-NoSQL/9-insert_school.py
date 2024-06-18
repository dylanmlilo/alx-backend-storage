#!/usr/bin/env python3
""" MongoDB Operations with Python using pymongo """


def insert_school(mongo_collection, **kwargs):
    """ Inserts a new document in a collection """
    new_doc = kwargs
    result = mongo_collection.insert_one(new_doc)
    return result.inserted_id
