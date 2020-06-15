import os

from dotenv import load_dotenv

from app import create_app
from app.extensions import mongoengine
from scripts.data_collection import init_collection_data
from scripts.seeds import seed_resource_graph

load_dotenv()

app = create_app(os.getenv('FLASK_CONFIG'))


@app.cli.command('data-collection', help='Script to get and generate data about system')
def get_data_collection() -> None:
    init_collection_data()


@app.cli.command('seed', help='Script to generate Resource Graphs')
def seed() -> None:
    seed_resource_graph()


@app.shell_context_processor
def make_shell_context() -> dict:
    return {'app': app, 'mongoengine': mongoengine}


if __name__ == '__main__':
    app.run()
