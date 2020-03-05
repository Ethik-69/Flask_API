"""Flask CLI/Application entry point."""
import os

import click

from flask_api import create_app, db
from flask_api.models.token_blacklist import BlacklistedToken
from flask_api.models.user import User
from flask_api.models.widget import Widget


app = create_app(os.getenv("FLASK_ENV", "development"))


# This decorator makes the decorated method execute
# when the flask shell command is run.
# https://aaronluna.dev/series/flask-api-tutorial/part-1/#flask-cliapplication-entry-point
@app.shell_context_processor
def shell():
    return {
        "db": db,
        "User": User,
        "BlacklistedToken": BlacklistedToken,
        "Widget": Widget,
    }


@app.cli.command("add-user", short_help="add a new user")
@click.argument("email")
@click.option(
    "--admin", is_flag=True, default=False, help="New user has administrator role"
)
@click.password_option(help="Do not set password on the command line!")
def add_user(email, admin, password):
    """Add a new user to the database with email address = EMAIL."""
    if User.find_by_email(email):
        error = f"Error: {email} is already registered"
        click.secho(f"{error}\n", fg="red", bold=True)
        return 1

    new_user = User(email=email, password=password, admin=admin)
    db.session.add(new_user)
    db.session.commit()
    user_type = "admin user" if admin else "user"
    message = f"Successfully added new {user_type}:\n {new_user}"
    click.secho(message, fg="blue", bold=True)
    return 0


if __name__ == "__main__":
    app.run()
