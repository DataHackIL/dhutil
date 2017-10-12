"""Email related utils for DataHack's registration system."""

import os
import json
import smtplib


CRED_DIR_PATH = os.path.expanduser('~/.datahack/')
CRED_FNAME = 'email_credentials.json'


def _get_credentials():
    fpath = os.path.join(CRED_DIR_PATH, CRED_FNAME)
    with open(fpath, 'r') as cred_file:
        return json.load(cred_file)


def send_email(from_addr, to_addrs, cc_addrs, bcc_addrs, subject, msg):
    """Sends an email from a DataHack email address.

    Arguments
    ---------
    from_addr : str
        The address presented as source address of the email.
    to_addrs : list
        A list of email addresses the email is sent to.
    cc_addres : list
        A list of email addresses CCed on the email.
    bcc_addres : list
        A list of email addresses BCCed on the email.
    subject : str
        The subject of the email.
    msg : str
        The body of the email.
    """
    cred = _get_credentials()
    server = smtplib.SMTP('{host}:{port}'.format(
        host=cred['host'], port=cred['port']))
    server.ehlo()
    server.starttls()
    server.login(cred['usr'], cred['pwd'])
    full_msg = "\r\n".join([
        "From: {}".format(from_addr),
        "To: {}".format(', '.join(to_addrs)),
        # This should NOT be included, otherwise it is shown in the email
        # "Bcc: {}".format(', '.join(bcc_addrs)),
        "Subject: {}".format(subject),
        "",
        msg
    ])
    server.sendmail(from_addr, to_addrs + bcc_addrs, full_msg)
    server.quit()
