"""MongoDB related commands for dhutil's CLI."""

import click

from dhutil.mongo_ops import (
    print_user_stats,
)


@click.group(help="MongoDB related commands.")
def mongo():
    """MongoDB related commands."""
    pass


@mongo.command(help="Print user stats.")
def user_stats():
    """Print user stats."""
    print_user_stats()
