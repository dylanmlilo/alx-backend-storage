#!/usr/bin/env python3
""" MongoDB Operations with Python using pymongo """


def list_all(mongo_collection):
    """ Lists all documents in a collection """
    documents = mongo_collection.find()
    return list(documents)
