"""MongoDB related commands for dhutil's CLI."""

import click

from dhutil.mongo_ops import (
    print_user_stats,
    dump_users_collection,
    dump_teams_collection,
)


@click.group(help="MongoDB related commands.")
def mongo():
    """MongoDB related commands."""
    pass


@mongo.command(help="Print user stats.")
def user_stats():
    """Print user stats."""
    print_user_stats()


@mongo.command(help="Dump the users collection.")
@click.option('--output', '-o', type=str)
def dump_users(output):
    """Dump the users collection."""
    dump_users_collection(output)

@mongo.command(help="Dump the teams collection.")
@click.option('--output', '-o', type=str)
def dump_teams(output):
    """Dump the teams collection."""
    dump_teams_collection(output)
