"""Python based utilities for the registration system."""

import os
import json
from urllib.parse import quote_plus
from functools import lru_cache

import pymongo


CRED_DIR_PATH = os.path.expanduser('~/.datahack/')
CRED_FNAME = 'mongodb_credentials.json'


def _get_credentials():
    fpath = os.path.join(CRED_DIR_PATH, CRED_FNAME)
    with open(fpath, 'r') as cred_file:
        return json.load(cred_file)


MONGODB_URI = "mongodb://{usr}:{pwd}@{host}:{port}"


def _get_mongodb_uri():
    cred = _get_credentials()
    return MONGODB_URI.format(
        usr=quote_plus(cred['usr']),
        pwd=quote_plus(cred['pwd']),
        host=cred['host'],
        port=cred['port'],
    )


@lru_cache(maxsize=2)
def _get_mongodb_client():
    cred = _get_credentials()
    return pymongo.MongoClient(
        host=_get_mongodb_uri(),
        authSource=cred['authSource'],
    )


def _get_mongo_database():
    return _get_mongodb_client()['datahack']


def get_users_collection():
    """Returns the DataHack users collection."""
    return _get_mongo_database()['users']
