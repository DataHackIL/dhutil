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


def get_spreadsheet_as_dataframe(worksheet_obj):
    list_of_lists = worksheet_obj.get_all_values()
    headers = list_of_lists[0]
    list_of_lists = list_of_lists[1:]
    list_of_lists = _cut_to_headers(list_of_lists, headers)
    return pd.DataFrame(list_of_lists, columns=headers)


def get_drive_users_worksheet():
    """Returns the users worksheet object."""
    cfg = _get_gdrive_cfg()
    spreadsheet_key = cfg['users_spreadsheet_key']
    worksheet_name = cfg['users_worksheet_name']
    gspread = get_authenticated_gspread()
    dh_users = gspread.open_by_key(spreadsheet_key)
    return dh_users.worksheet(worksheet_name)


def get_drive_users_dataframe():
    """Returns the content of the users spreadsheet as a pandas DataFrame."""
    return get_spreadsheet_as_dataframe(get_drive_users_worksheet())


ABC_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def num_to_letter(num):
    try:
        return ABC_LETTERS[num-1]
    except IndexError:
        return 'A'+ num_to_letter(num-26)


def header_to_letter(worksheet):
    headers = worksheet.row_values(1)
    return {header: num_to_letter(i+1) for i, header in enumerate(headers)}


def header_to_number(worksheet):
    headers = worksheet.row_values(1)
    return {header: i+1 for i, header in enumerate(headers)}


def get_emails_from_worksheet(worksheet):
    header_to_num = header_to_number(worksheet)
    emails_col = worksheet.col_values(header_to_num['email'])
    emails_col = emails_col[1:]
    return [email for email in emails_col if email != '']
