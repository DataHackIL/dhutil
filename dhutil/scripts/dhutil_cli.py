"""A command-line interface for dhutil."""

import click

from .mail_cli import mail
from .mongo_cli import mongo
from .mailchimp_cli import mailchimp
from .drive_cli import drive


@click.group(help="A command-line interface for dhutil.")
def cli():
    """A command-line interface for dhutil."""
    pass


cli.add_command(mail)
cli.add_command(mongo)
cli.add_command(mailchimp)
cli.add_command(drive)
