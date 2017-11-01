"""Python based utilities for DataHack."""

import os
import csv
from subprocess import call
from itertools import zip_longest

from tqdm import tqdm
from mongozen.queries.common import key_value_counts

from .mongo_utils import (
    _get_mongo_database,
)
from .mail_ops import CONFIRM_FIELD_NAME


def pprint_ordered_dict(odict):
    max_key_len = max([len(str(key)) for key in odict])
    item_fmt_str = '  {'+':{}'.format(max_key_len+1)+'}: {}'
    # print(item_fmt_str)
    for key in odict:
        print(item_fmt_str.format(key, odict[key]))


def pprint_two_ordered_dicts(name1, odict1, name2, odict2):
    max_key_len1 = max([len(str(key)) for key in odict1])
    max_key_len2 = max([len(str(key)) for key in odict2])
    max_val_len1 = max([len(str(odict1[key])) for key in odict1])
    header_fmt_str = '  ={}={' + ':{}'.format(
        max_key_len1+max_val_len1+1)+'}={}='
    # print(header_fmt_str)
    line_fmt_str = '  {'+':{}'.format(
        max_key_len1+1)+'}: {'+':{}'.format(
            max_val_len1+1)+'}     {'+':{}'.format(
                max_key_len2+1)+'}: {}'
    # print(line_fmt_str)
    print(header_fmt_str.format(name1, '', name2))
    for key1, key2 in zip_longest(odict1.keys(), odict2.keys(), fillvalue=''):
        print(line_fmt_str.format(
            key1, odict1.get(key1, ''), key2, odict2.get(key2, '')))


def print_user_stats():
    users = _get_mongo_database()['users']
    print("{} total users in the system.".format(users.count()))
    print("{} users got a confirmation email.".format(
        users.count({CONFIRM_FIELD_NAME: True})))
    pprint_two_ordered_dicts(
        'Gender', key_value_counts('gender', users),
        'Food', key_value_counts('food', users),
    )
    pprint_two_ordered_dicts(
        'Sleep', key_value_counts('sleep', users),
        'Transport', key_value_counts('transport', users),
    )
    pprint_two_ordered_dicts(
        'Workshop', key_value_counts('workshop', users),
        'TLV Bus', key_value_counts('bus', users),
    )
    pprint_two_ordered_dicts(
        'Class', key_value_counts('class', users),
        'Shirt size', key_value_counts('shirtsize', users),
    )
    pprint_two_ordered_dicts(
        'Student', key_value_counts('student', users),
        'Hacker', key_value_counts('hacker', users),
    )
    pprint_two_ordered_dicts(
        'Team Status', key_value_counts('teamstatus', users),
        'Newsletter', key_value_counts('newsletter', users),
    )


def dump_collection(collection_name, field_names, output_folder_path):
    """Dump the given collection."""
    collection = _get_mongo_database()[collection_name]
    count = collection.count()
    cursor = collection.find(
        filter={},
        projection={'_id': 0, **{name: 1 for name in field_names}},
    )
    fpath = os.path.join(output_folder_path, 'dh_{}.csv'.format(
        collection_name))
    with tqdm(total=count) as pbar:
        with open(fpath, 'w+') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=field_names)
            writer.writeheader()
            for x in cursor:
                writer.writerow(x)
                pbar.update(1)


USERS_FIELD_NAMES = [
    'first_name', 'last_name', 'gender', 'email', 'degree', 'field',
    'institution', 'teamstatus', 'team', 'workshop', 'bus', 'hacker',
    'shirttype', 'shirtsize', 'food', 'sleep', 'student', 'class', 'transport'
    'newsletter', 'age', 'phone', 'regDate', 'tags',
]

def dump_users_collection(output_folder_path):
    """Dump the users collection."""
    dump_collection('users', USERS_FIELD_NAMES, output_folder_path)


TEAMS_FIELD_NAMES = [
    'team_name', 'admin_email', 'members', 'isClosed', 'idea', 'challenge',
    'dataset', 'lookingText', 'tags',
]

def dump_teams_collection(output_folder_path):
    """Dump the teams collection."""
    dump_collection('teams', TEAMS_FIELD_NAMES, output_folder_path)
