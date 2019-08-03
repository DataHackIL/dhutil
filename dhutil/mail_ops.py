"""Python based utilities for DataHack."""

from dhutil.mongo_utils import (
    _get_mongo_database,
)
from dhutil.mail_utils import (
    send_email,
)
from dhutil.shared import (
    IS_ACCEPTED_FIELD_NAME,
)

YEAR = 2019
STATIC_WEBSITE = 'https://www.datahack.org.il'
REG_WEBSITE = 'https://registration.datahack.org.il'
def _print_email_stats():
    users = _get_mongo_database()['users']
    print(f"Emails stats on DataHack {YEAR} registration:")
    print("{} total users in the system.".format(users.count_documents({})))
    print("{} users got a confirmation email.".format(users.count({CONFIRM_FIELD_NAME: True})))
    print("{} users got an acceptance email.".format(users.count({ACCEPT_FIELD_NAME: True})))


def _set_field_true_by_emails(emails, field_name):
    if field_name:
        users = _get_mongo_database()['users']
        users.update_many(
            filter={'email': {'$in': emails}},
            update={'$set': {field_name: True}},
        )


def _send_batch_email(emails, subject, body, field_name):
    print("Sending a batch email to the following addresses:")
    print(emails)
    send_email(
        from_addr="contact@datahack.org.il",
        to_addrs=["contact@datahack-il.com"],
        cc_addrs=[],
        bcc_addrs=emails,
        subject=subject,
        msg=body,
    )
    print("Email sent successfully")
    _set_field_true_by_emails(emails, field_name)
    print('Marked {} as true for these users on MongoDB\n'.format(field_name))


ZOHO_MAX_RECIPIENTS = 50
ZOHO_MAX_DAILY_MAILS = 150


def send_batch_emails(emails, subject, body, field_name):
    batch = []
    total = 0
    email_count = 0
    emails_iter = iter(emails)
    while True:
        try:
            email = emails_iter.__next__()
            batch.append(email)
            total += 1
            if len(batch) == ZOHO_MAX_RECIPIENTS:
                _send_batch_email(batch, subject, body, field_name)
                email_count += 1
                batch = []
        except StopIteration:
            if batch:
                _send_batch_email(batch, subject, body, field_name)
                email_count += 1
            break
    print(f"\n==========\n{email_count} emails were sent to {total} users.")


CONFIRM_FIELD_NAME = 'confirmation_email'
CONFIRM_SUBJECT = f'Your are now registered for DataHack {YEAR}'
CONFIRM_BODY = f"""
You have successfully registered for DataHack {YEAR}!
This does not yet confirm your participation in the event.

What Now?
* Sit tight
* Brush your hacking skills
* Patiently wait for a confirmation mail saying you've been accepted.
This will probably happen a few days after registration is closed.

Thanks,
DataHack {YEAR} Team
"""


def send_confirmation_emails():
    _print_email_stats()
    print("Sending confirmation emails to all non-confirmed users.")
    users = _get_mongo_database()['users']
    users_to_send = list(users.find(
        filter={CONFIRM_FIELD_NAME: {'$ne': True}},
        projection={'email': 1}
    ))
    emails = [doc['email'] for doc in users_to_send]
    send_batch_emails(
        emails, CONFIRM_SUBJECT, CONFIRM_BODY, CONFIRM_FIELD_NAME)


ACCEPT_FIELD_NAME = 'acceptance_email'
ACCEPT_SUBJECT = f"You have been accepted to DataHack {YEAR}!"
ACCEPT_BODY = (
f'''This is a message confirming you have been accepted to DataHack {YEAR}!
If you still don't have a team - that's ok! You don't have to have a team \
to attend DataHack {YEAR}. However, working together is fun, so take a \
look at the open teams page and send an email to captains of teams you \
would like to join:
{REG_WEBSITE}/mingle
If you need more information about the event visit us at 
{STATIC_WEBSITE}/ !

You can also read frequently asked questions (and answers) here: 
{STATIC_WEBSITE}/faq

Finally, you can hit us at contact@datahack.co.il with questions.


More information coming soon,
The DataHack Team'''
)


def send_acceptance_emails():
    _print_email_stats()
    print("Sending acceptance emails to accepted users who didn't get one.")
    users = _get_mongo_database()['users']
    users_to_send = list(users.find(
        filter={
            IS_ACCEPTED_FIELD_NAME: True,
            ACCEPT_FIELD_NAME: {'$ne': True},
        },
        projection={'email': True}
    ))
    emails = [doc['email'] for doc in users_to_send]
    print("Found {} users who need them...".format(len(emails)))
    send_batch_emails(
        emails, ACCEPT_SUBJECT, ACCEPT_BODY, ACCEPT_FIELD_NAME)
