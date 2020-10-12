import os

from dotenv import load_dotenv

from app import create_app
from app.models import (Resource as ResourceModel,
                        ResourceField as ResourceFieldModel)
from scripts.init_db import init_db
from scripts.fill_resource_data import fill_resource_data

load_dotenv()

app = create_app(os.getenv('FLASK_CONFIG'))


@app.cli.command('init-db',
                 help='Create required database schema and data.')
def db() -> None:
    """Create required database schema and data."""
    init_db()


@app.cli.command('data-collection',
                 help='Getting server information for saving a '
                      'Resource document.')
def get_data_collection() -> None:
    """Getting server information for saving a Resource document."""
    fill_resource_data()


@app.shell_context_processor
def make_shell_context() -> dict:
    """Returns the shell context for an interactive shell for this application.
    This runs all the registered shell context processors.

    To explore the data in your application, you can start an interactive Python
    shell with the shell command. An application context will be active,
    and the app instance will be imported.

    How to usage::

        source venv/bin/activate
        flask shell

    .. _shell_context_processor:
        https://flask.palletsprojects.com/en/1.1.x/cli/#open-a-shell

    Returns
    -------
    dict
        Imports available in Python shell.

    """
    return {'app': app, 'Resource': ResourceModel,
            'ResourceField': ResourceFieldModel}


if __name__ == '__main__':
    app.run()
