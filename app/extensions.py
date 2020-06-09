from flask import Flask
from flask_graphql import GraphQLView
from flask_mongoengine import MongoEngine


mongoengine = MongoEngine()

def init_app(app: Flask) -> None:
    from .schema import schema

    mongoengine.init_app(app)

    app.add_url_rule(
        '/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
    )
