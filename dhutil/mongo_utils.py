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




def _get_mongodb_uri():
    cred = _get_credentials()
    srv = cred['srv']
    if srv:
        uri = 'mongodb+srv://{usr}:{pwd}@{host}/{authSource}'
    else:
        uri = 'mongodb://{usr}:{pwd}@{host}:{port}/{authSource}'
    uri = uri.format_map(cred)
    return uri


@lru_cache(maxsize=2)
def _get_mongodb_client():
    URI = _get_mongodb_uri()
    client = pymongo.MongoClient(URI)
    return client


def _get_mongo_database():
    cred = _get_credentials()
    return _get_mongodb_client()[cred['db']]


def get_users_collection(sandbox=False):
    """Returns the DataHack users collection."""
    return _get_mongo_database()['users']
