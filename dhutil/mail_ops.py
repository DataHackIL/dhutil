"""Python based utilities for DataHack."""
import re

from dhutil.mongo_utils import (
    _get_mongo_database,
)
from dhutil.mail_utils import (
    send_email,
)
from dhutil.shared import (
    IS_ACCEPTED_FIELD_NAME,
    IS_ACCEPTED_DATALEARN_FIELD_NAME,
    IS_REGISTER_DATALEARN_FIELD_NAME,
    IS_REJECTED_FIELD_NAME,
    ACCEPT_EMAIL_FIELD_NAME)
import pathlib

CURDIR = pathlib.Path(__file__).parent
TEMPLATES = CURDIR / 'mail_templates'

YEAR = 2019
STATIC_WEBSITE = 'https://www.datahack.org.il'
REG_WEBSITE = 'https://registration.datahack.org.il'

INFO = dict(YEAR=YEAR, STATIC_WEBSITE=STATIC_WEBSITE, REG_WEBSITE=REG_WEBSITE)
ZOHO_MAX_RECIPIENTS = 50
ZOHO_MAX_DAILY_MAILS = 150
FALSE = {'$ne': True}

def _print_email_stats():
    users = _get_mongo_database()['users']
    print(f"Emails stats on DataHack {YEAR} registration:")
    print("{} total users in the system.".format(users.count_documents({})))
    print("{} users got a confirmation email.".format(users.count({CONFIRM_FIELD_NAME: True})))
    print("{} users got an acceptance email.".format(users.count({ACCEPT_EMAIL_FIELD_NAME: True})))


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


def _get_body(filename):
    with open(TEMPLATES / filename, 'r') as f:
        body = f.read().format_map(INFO)
    body = re.sub(u"(\u2018|\u2019)","",body)
    return body


def send_acceptance_emails(sandbox=False):
    if not sandbox:
        sandbox = FALSE
    _print_email_stats()
    print("Sending acceptance emails to accepted users who didn't get one.")
    users = _get_mongo_database()['users']
    users_to_send = list(users.find(
        filter={
            'sandbox': sandbox,
            IS_ACCEPTED_FIELD_NAME: True,
            IS_ACCEPTED_DATALEARN_FIELD_NAME: FALSE,
            IS_REJECTED_FIELD_NAME: FALSE,
            IS_REGISTER_DATALEARN_FIELD_NAME: FALSE,
            ACCEPT_EMAIL_FIELD_NAME: FALSE,
        },
        projection={'email': True}
    ))
    emails = [doc['email'] for doc in users_to_send]
    print("Found {} relevant users".format(len(emails)))
    subject = f"You have been accepted to DataHack {YEAR}!"
    body = _get_body('accepted.txt')
    send_batch_emails(emails, subject, body, ACCEPT_EMAIL_FIELD_NAME)

def send_acceptance_datalearn_emails(sandbox=False):
    if not sandbox:
        sandbox = FALSE
    print("Sending acceptance DATALEARN emails to accepted users who didn't get one.")
    users = _get_mongo_database()['users']
    users_to_send = list(users.find(
        filter={
            'sandbox': sandbox,
            IS_ACCEPTED_FIELD_NAME: FALSE,
            IS_ACCEPTED_DATALEARN_FIELD_NAME: True,
            IS_REJECTED_FIELD_NAME: FALSE,
            IS_REGISTER_DATALEARN_FIELD_NAME: True,
            ACCEPT_EMAIL_FIELD_NAME: FALSE,
        },
        projection={'email': True}
    ))
    emails = [doc['email'] for doc in users_to_send]
    print("Found {} relevant users".format(len(emails)))
    subject = f"You have been accepted to DataLearn {YEAR}!"
    body = _get_body('acceptedWorkshop.txt')
    send_batch_emails(emails, subject, body, ACCEPT_EMAIL_FIELD_NAME)

def send_acceptance_upgrade_emails(sandbox=False):
    if not sandbox:
        sandbox = FALSE
    print("Sending acceptance DATALEARN UPGRADE emails to accepted users who didn't get one.")
    users = _get_mongo_database()['users']
    users_to_send = list(users.find(
        filter={
            'sandbox': sandbox,
            IS_ACCEPTED_FIELD_NAME: True,
            IS_ACCEPTED_DATALEARN_FIELD_NAME: FALSE,
            IS_REJECTED_FIELD_NAME: FALSE,
            IS_REGISTER_DATALEARN_FIELD_NAME: True,
            ACCEPT_EMAIL_FIELD_NAME: FALSE,
        },
        projection={'email': True}
    ))
    emails = [doc['email'] for doc in users_to_send]
    print("Found {} relevant users".format(len(emails)))
    subject = f"You have been accepted to DataHack {YEAR}! Main Competition"
    body = _get_body('upgrade.txt')
    send_batch_emails(emails, subject, body, ACCEPT_EMAIL_FIELD_NAME)

def send_rejection_upgrade_emails(sandbox=False):
    if not sandbox:
        sandbox = FALSE
    print("Sending acceptance DATALEARN emails to accepted users who didn't get one.")
    users = _get_mongo_database()['users']
    users_to_send = list(users.find(
        filter={
            'sandbox': sandbox,
            IS_ACCEPTED_FIELD_NAME: FALSE,
            IS_ACCEPTED_DATALEARN_FIELD_NAME: FALSE,
            IS_REJECTED_FIELD_NAME: True,
            ACCEPT_EMAIL_FIELD_NAME: FALSE,
        },
        projection={'email': True}
    ))
    emails = [doc['email'] for doc in users_to_send]
    print("Found {} relevant users".format(len(emails)))
    subject = f"Sorry! You have not been accepted DataHack {YEAR}!"
    body = _get_body('rejected.txt')
    send_batch_emails(emails, subject, body, ACCEPT_EMAIL_FIELD_NAME)