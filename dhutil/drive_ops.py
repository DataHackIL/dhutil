"""Google Drive operations."""

from tqdm import tqdm

from .drive_utils import (
    get_drive_users_worksheet,
    get_drive_conf_worksheet,
    get_drive_users_dataframe,
    get_col_from_worksheet,
    get_emails_from_worksheet,
    header_to_number,
)
from .mongo_utils import (
    get_users_collection,
)
from .mail_ops import (
    send_batch_emails,
)
from .shared import (
    IS_ACCEPTED_FIELD_NAME,
)


def sync_google_drive_acceptance_status_to_mongo():
    """Syncs the acceptance status of users from Google Drive to MongoDB."""
    print("Getting users spreadsheet from Google Drive...")
    users_df = get_drive_users_dataframe()
    print("Total of {} users in spreadsheet.".format(len(users_df)))
    users_df['status'] = users_df['status'].str.lower()
    accepted = users_df[users_df['status'] == 'yes']
    print("Total of {} accepted users in spreadsheet.".format(len(accepted)))
    not_accepted = users_df[users_df['status'] == 'no']
    print("Total of {} not accepted users in spreadsheet.".format(
        len(not_accepted)))
    cant_come = users_df[users_df['status'] == "can't come"]
    print("Total of {} can't come users in spreadsheet.".format(
        len(cant_come)))
    accepted_emails = list(accepted['email'])
    not_accepted_emails = list(not_accepted['email'])
    cant_come_emails = list(cant_come['email'])
    print("Updating acceptance status to MongoDB.")
    users = get_users_collection()
    users.update_many(
        filter={'email': {'$in': accepted_emails}},
        update={'$set': {IS_ACCEPTED_FIELD_NAME: True}}
    )
    users.update_many(
        filter={'email': {'$in': not_accepted_emails}},
        update={'$set': {IS_ACCEPTED_FIELD_NAME: False}}
    )
    users.update_many(
        filter={'email': {'$in': cant_come_emails}},
        update={'$set': {IS_ACCEPTED_FIELD_NAME: False}}
    )
    print("Done.")


def sync_uptodate_teams_from_mongo():
    """Syncs the up-to-date team of each registrant from MongoDB to Drive."""
    print("Getting users spreadsheet from Google Drive...")
    users = get_drive_users_worksheet()
    print("Getting emails from worksheet...")
    emails = get_emails_from_worksheet(users)
    print("Total of {} users in spreadsheet.".format(len(emails)))
    mongo_users = get_users_collection()
    all_users = mongo_users.find()
    email_to_team = {}
    print("Building email to team map from MongoDB...")
    for user_doc in all_users:
        email_to_team[user_doc['email']] = user_doc['team']
    print("Email to team map built.", flush=True)
    header_to_num = header_to_number(users)
    team_header_num = header_to_num['team']
    for i, email in tqdm(enumerate(emails)):
        email_row = i + 2
        try:
            uptodate_team = email_to_team[email]
            # print("I want to update cell {}, {} with {}".format(
                # email_row, team_header_num, uptodate_team))
            users.update_cell(email_row, team_header_num, uptodate_team)
        except KeyError:
            print("No mapping found for email {}.".format(email), flush=True)


CONF_CONFIRM_SUBJECT = "Your registration to DataConf 2017 is confirmed!"
CONF_CONFIRM_BODY = (
    "Your registration to DataConf 2017 has been processed successfully.\n"
    "We are looking forward to seeing you this coming Thursday.\n"
    "Don't forget: The Alliance House, Ki'akh 5, Jerusalem. October 26th. "
    "9:00 to 18:00.\n\nYours,\nThe conferenc team."
)

def send_conf_confirm_emails():
    print("Getting DataConf worksheet...")
    conf = get_drive_conf_worksheet()
    print("Getting emails column...")
    emails = get_emails_from_worksheet(conf, 'your-email')
    print("{} regsitrants in spreadsheet.".format(len(emails)))
    print("Getting confirmation column...")
    confirm = get_col_from_worksheet(conf, 'confirm_email')
    confirm = confirm[:len(emails)]
    header_to_num = header_to_number(conf)
    confirm_header_num = header_to_num['confirm_email']
    emails_to_send = []
    indexes_to_set_true = []
    print("Getting people needing confirmation...")
    for i, email in tqdm(enumerate(emails)):
        email_row = i + 2
        confirmed = confirm[i]
        if confirmed != 'TRUE':
            emails_to_send.append(email)
            indexes_to_set_true.append(email_row)
    print("{} registrants need confirmation.".format(len(emails_to_send)))
    print("Sending batch emails...")
    send_batch_emails(
        emails=emails_to_send,
        subject=CONF_CONFIRM_SUBJECT,
        body=CONF_CONFIRM_BODY,
        field_name=None,
    )
    print("Setting confirmation status in spreadsheet...")
    for email_row in indexes_to_set_true:
        conf.update_cell(email_row, confirm_header_num, 'TRUE')
    print("All done.")
