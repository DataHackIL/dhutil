"""Email related commands for dhutil's CLI."""

import click

from dhutil.mail_ops import (
    _print_email_stats,
    send_confirmation_emails,
)


@click.group(help="Email related commands.")
def mail():
    """Email related commands."""
    pass


@mail.command(help="Status of confirmation emails.")
def confirm_stat():
    """Status of confirmation emails."""
    _print_email_stats()


@mail.command(help="Send confirmation emails.")
def confirm_send():
    """Send confirmation emails."""
    send_confirmation_emails()
