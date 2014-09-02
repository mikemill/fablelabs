import json
import os.path
from sqlalchemy import event
from sqlalchemy.orm import mapper

from flask.ext.sqlalchemy import SQLAlchemy

db = None
connection_string = None


def get_connection_string():
    config_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '..',
        'database.json'
    )

    with open(config_file) as f:
        config = json.load(f)

    connection_string = ''.join([
        'mysql://',
        config['user'],
        ':' + config['password'] if config['password'] else '',
        '@' + config['host'],
        '/' + config['database']
    ])

    return connection_string


def connect(app):
    global db

    app.config['SQLALCHEMY_DATABASE_URI'] = get_connection_string()
    db = SQLAlchemy(app)

    @app.teardown_request
    def autocommit(exception=None):
        db.session.commit()


def initialize_database(engine, session, base):
    base.metadata.bind = engine
    base.query = session.query_property()


@event.listens_for(mapper, 'init')
def auto_add_to_session(target, args, kwargs):
    db.session.add(target)
