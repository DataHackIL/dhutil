"""MongoDB related commands for dhutil's CLI."""

import click

from dhutil.drive_ops import (
    sync_google_drive_acceptance_status_to_mongo,
    sync_uptodate_teams_from_mongo,
    send_conf_confirm_emails,
)


@click.group(help="Google Drive related commands.")
def drive():
    """Google Drive related commands."""
    pass


_SYNC_ACCEPTED_MSG = "Sync Google Drive acceptance status to MongoDB"

@drive.command(help=_SYNC_ACCEPTED_MSG)
def sync_accepted():
    __doc__ = _SYNC_ACCEPTED_MSG # pylint: disable=W0622
    sync_google_drive_acceptance_status_to_mongo()


_SYNC_TEAM_MSG = "Sync Google Drive user team from MongoDB"

@drive.command(help=_SYNC_TEAM_MSG)
def sync_team():
    __doc__ = _SYNC_TEAM_MSG # pylint: disable=W0622
    sync_uptodate_teams_from_mongo()


_CONF_CONFORM_MSG = "Send DataConf confirmation email."

@drive.command(help=_CONF_CONFORM_MSG)
def conf_confirm():
    __doc__ = _CONF_CONFORM_MSG # pylint: disable=W0622
    send_conf_confirm_emails()
