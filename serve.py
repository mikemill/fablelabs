from flask import Flask

from app import database, utils
from app.models import load_models


def setup_routes(application):
    """Add the routes to the Flask application object"""

    # Do the controller import here after the models have been loaded
    from app.controllers import view_controller, api_controller

    # Some helpers to make defining the routes a bit cleaner
    def get(path, rule, func, *args, **kwargs):
        kwargs['methods'] = ['GET']
        application.add_url_rule(path, rule, func, *args, **kwargs)

    def post(path, rule, func, *args, **kwargs):
        kwargs['methods'] = ['POST']
        application.add_url_rule(path, rule, func, *args, **kwargs)

    get('/', 'index', view_controller.index)
    get('/upload', 'upload', view_controller.upload)
    get('/search', 'search', view_controller.search)

    post('/api/publish', 'api_publish', api_controller.publish)
    get('/api/search/<text>', 'api_search', api_controller.search)
    get('/api/search/', 'api_search_empty', api_controller.search)
    get('/api/get/<int:id>', 'api_get_file', api_controller.get_file)


if __name__ == '__main__':
    application = Flask(__name__)
    application.json_encoder = utils.AppJsonEncoder
    database.connect(application)
    load_models()
    setup_routes(application)

    application.run(debug=True)
