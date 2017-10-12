"""A command-line interface for dhutil."""

import click

from .mail_cli import mail


@click.group(help="A command-line interface for dhutil.")
def cli():
    """A command-line interface for dhutil."""
    pass


cli.add_command(mail)
