import os

from dotenv import load_dotenv

from app import create_app
from app.extensions import mongoengine
from scripts.data_collection import init_collection_data

load_dotenv()

app = create_app(os.getenv('FLASK_CONFIG'))


@app.cli.command('data-collection', help='TODO: WIP')
def get_data_collection() -> None:
    init_collection_data()


@app.shell_context_processor
def make_shell_context() -> dict:
    return {'app': app, 'mongoengine': mongoengine}


if __name__ == '__main__':
    app.run()
