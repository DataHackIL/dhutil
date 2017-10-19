"""Google Drive utils."""

import os
import json

import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials


DH_DIRPATH = os.path.expanduser('~/.datahack')
DRIVE_KEY_FNAME = 'google_drive_service_account_key.json'
DRIVE_KEY_FPATH = os.path.join(DH_DIRPATH, DRIVE_KEY_FNAME)

GOOGLE_DRIVE_SPREADSHEET_SCOPE_URL = 'https://spreadsheets.google.com/feeds'


def get_authenticated_gspread():
    """Returns an authenticated gspread instance."""
    scope = [GOOGLE_DRIVE_SPREADSHEET_SCOPE_URL]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        DRIVE_KEY_FPATH, scope)
    return gspread.authorize(credentials)


CFG_FNAME = 'google_drive_cfg.json'


def _get_gdrive_cfg():
    fpath = os.path.join(DH_DIRPATH, CFG_FNAME)
    with open(fpath, 'r') as cfg_file:
        return json.load(cfg_file)


def _cut_to_headers(list_of_lists, headers_list):
    return [sublist[:len(headers_list)] for sublist in list_of_lists]


def get_spreadsheet_as_dataframe(spreadsheet, worksheet_name):
    worksheet_obj = spreadsheet.worksheet(worksheet_name)
    list_of_lists = worksheet_obj.get_all_values()
    headers = list_of_lists[0]
    list_of_lists = list_of_lists[1:]
    list_of_lists = _cut_to_headers(list_of_lists, headers)
    return pd.DataFrame(list_of_lists, columns=headers)


def get_drive_users_dataframe():
    """Returns the content of the users spreadsheet as a pandas DataFrame."""
    cfg = _get_gdrive_cfg()
    spreadsheet_key = cfg['users_spreadsheet_key']
    worksheet_name = cfg['users_worksheet_name']
    gspread = get_authenticated_gspread()
    dh_users = gspread.open_by_key(spreadsheet_key)
    return get_spreadsheet_as_dataframe(dh_users, worksheet_name)
