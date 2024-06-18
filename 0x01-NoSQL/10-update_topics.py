#!/usr/bin/env python3
""" Updates all topics of a school document """


def update_topics(mongo_collection, name, topics):
    """ Updates all topics of a school document """
    result = mongo_collection.update_one(
        {"name": name},
        {"$set": {"topics": topics}}
    )
    return result.modified_count
