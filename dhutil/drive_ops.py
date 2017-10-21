"""Google Drive operations."""

from tqdm import tqdm

from .drive_utils import (
    get_drive_users_worksheet,
    get_drive_users_dataframe,
    get_emails_from_worksheet,
    header_to_number,
)
from .mongo_utils import (
    get_users_collection,
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
    accepted_emails = list(accepted['email'])
    print("Updating acceptance status to MongoDB.")
    users = get_users_collection()
    users.update_many(
        filter={'email': {'$in': accepted_emails}},
        update={'$set': {IS_ACCEPTED_FIELD_NAME: True}}
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
