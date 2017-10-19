"""Google Drive operations."""

from .drive_utils import (
    get_drive_users_dataframe,
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
