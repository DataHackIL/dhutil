"""Mailchimp-related DataHack utils."""

import os
import json
import pprint
import requests

from tqdm import tqdm
from decore import lazy_property
from mailchimp3 import MailChimp

from .mongo_utils import _get_mongo_database
from .shared import IS_ACCEPTED_FIELD_NAME



CRED_DIR_PATH = os.path.expanduser('~/.datahack/')
CRED_FNAME = 'mailchimp_credentials.json'


def _get_credentials():
    fpath = os.path.join(CRED_DIR_PATH, CRED_FNAME)
    with open(fpath, 'r') as cred_file:
        return json.load(cred_file)


@lazy_property
def get_mailchimp_client():
    """Returns a mailchimp3.MailChimp client object."""
    cred = _get_credentials()
    return MailChimp(cred['username'], cred['secret_key'], timeout=100)


def list_lists():
    """List mailchimp lists."""
    client = get_mailchimp_client()
    lists = client.lists.all(get_all=True, fields="lists.name,lists.id")
    pprint.pprint(lists)


@lazy_property
def _registrants_list_id():
    cred = _get_credentials()
    return cred['registrants_list_id']


@lazy_property
def _accepted_list_id():
    cred = _get_credentials()
    return cred['accepted_list_id']


def _get_all_emails_by_list_id(list_id):
    client = get_mailchimp_client()
    result = client.lists.members.all(
        list_id, get_all=True, fields="members.email_address")
    return [item['email_address'] for item in result['members']]


def _add_user_to_registrants_list(user):
    # print(user)
    client = get_mailchimp_client()
    data = {
        'email_address': user['email'],
        'status': 'subscribed',
        'update_existing': True,
        'send_welcome': False,
        'merge_fields': {
            'FNAME': str(user['first_name']),
            'LNAME': str(user['last_name']),
            'GENDER': str(user['gender']),
            'STUDENT': str(user['student']),
            'FOOD': str(user['food']),
            'SLEEP': str(user['sleep']),
            'TRANSPORT': str(user['transport']),
            'WORKSHOP': str(user['workshop']),
            'BUS': str(user['bus']),
        },
    }
    try:
        client.lists.members.create(_registrants_list_id(), data)
    except requests.exceptions.HTTPError:
        print('Adding user with the following data failed:')
        print(data)
        # data['merge_fields']['FNAME'] = '<Hebrew_string>'
        # data['merge_fields']['LNAME'] = '<Hebrew_string>'
        # data['email_address'] = user['email'].lower()
        # print(data)
        # try:
        #     client.lists.members.create(_registrants_list_id(), data)
        #     print('After removing Hebrew strings it worked!')
        # except requests.exceptions.HTTPError:
        #     print("Didn't work. Moving on.")


def sync_mailchimp_registrants():
    """Sync the MailChimp registrants list with registration DB."""
    print("Syncing the MailChimp registrants list with registration DB.")
    users = _get_mongo_database()['users']
    emails_in_list = _get_all_emails_by_list_id(_registrants_list_id())
    users_to_add = users.find({'email': {'$nin': emails_in_list}})
    num_users_to_add = users.count({'email': {'$nin': emails_in_list}})
    with tqdm(total=num_users_to_add) as pbar:
        for user in users_to_add:
            _add_user_to_registrants_list(user)
            pbar.update(1)


def _add_user_to_accepted_list(user):
    # print(user)
    client = get_mailchimp_client()
    data = {
        'email_address': user['email'],
        'status': 'subscribed',
        'update_existing': True,
        'send_welcome': False,
        'merge_fields': {},
    }
    try:
        client.lists.members.create(_accepted_list_id(), data)
    except requests.exceptions.HTTPError:
        print('Adding user with the following data failed:')
        print(data)


def sync_mailchimp_accepted():
    """Sync the MailChimp accepted list with registration DB."""
    print("Syncing the MailChimp accepted list with registration DB.")
    users = _get_mongo_database()['users']
    emails_in_list = _get_all_emails_by_list_id(_accepted_list_id())
    accepted_to_add_matchop = {
        IS_ACCEPTED_FIELD_NAME: True,
        'email': {'$nin': emails_in_list}
    }
    users_to_add = users.find(accepted_to_add_matchop)
    num_users_to_add = users.count(accepted_to_add_matchop)
    with tqdm(total=num_users_to_add) as pbar:
        for user in users_to_add:
            _add_user_to_accepted_list(user)
            pbar.update(1)
