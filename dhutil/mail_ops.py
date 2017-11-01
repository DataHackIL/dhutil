"""Python based utilities for DataHack."""

from .mongo_utils import (
    _get_mongo_database,
)
from .mail_utils import (
    send_email,
)
from .shared import (
    IS_ACCEPTED_FIELD_NAME,
)


def _print_email_stats():
    users = _get_mongo_database()['users']
    print("Emails stas on DataHack 2017 registration:")
    print("{} total users in the system.".format(users.count()))
    print("{} users got a confirmation email.".format(
        users.count({CONFIRM_FIELD_NAME: True})))
    print("{} users got an acceptance email.".format(
        users.count({ACCEPT_FIELD_NAME: True})))


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
        from_addr="contact@datahack-il.com",
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
    print("\n==========\n{} emails were sent to {} users.".format(
        email_count, total))


CONFIRM_FIELD_NAME = 'confirmation_email'
CONFIRM_SUBJECT = "Your registration for DataHack 2017 is confirmed!"
CONFIRM_BODY = (
    "This is a message confirming you registration form for DataHack 2017"
    " has been processed.\n This does not confirm your participation in the"
    " event. Confirmation emails for participation will go out at a later"
    " date."
)


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
ACCEPT_SUBJECT = "You have been accepted to DataHack 2017!"
ACCEPT_BODY = (
    "This is a message confirming you have been accepted to DataHack 2017!\n\n"
    "If you still don't have a team - that's ok! You don't have to have a team"
    " to attend DataHack 2017. However, working together is fun, so take a "
    "look at the open teams page and send an email to captains of teams you "
    "would like to join:\nhttp://register.datahack-il.com/mingle\n"
    "If you need more information about the event visit us at "
    "http://datahack-il.com/ !\n"
    "You can also read frequently asked questions (and answers) here: "
    "http://datahack-il.com/faq.html \n"
    "Finally, you can hit us at contact@datahack-il.com with questions.\n\n"
    "More information coming soon,\nThe DataHack Team"
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
        projection={'email': 1}
    ))
    emails = [doc['email'] for doc in users_to_send]
    print("Found {} users who need them...".format(len(emails)))
    send_batch_emails(
        emails, ACCEPT_SUBJECT, ACCEPT_BODY, ACCEPT_FIELD_NAME)
