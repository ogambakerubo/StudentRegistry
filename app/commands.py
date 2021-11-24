from flask import Flask, Blueprint

from app.db_con import create_tables, super_user, destroy_tables

commands = Blueprint("commands", __name__)


@commands.cli.command("create-tables")
def create_tbs():
    """create tables"""
    create_tables()


@commands.cli.command("create-admin")
def create_admin():
    """create super user"""
    super_user()


@commands.cli.command("destroy-tables")
def destroy_tbs():
    """destroy tables"""
    destroy_tables()
