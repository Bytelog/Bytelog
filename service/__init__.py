import os

from .assets import AssetManager
from .config import Development
from .config import Production
from .document import Documents
from flask import Flask
from flask import render_template

am = AssetManager('assets', 'public')
documents = Documents('content', 'templates/cache')


def create_app():
    app = Flask(
        __name__.split('.')[0],
        template_folder='../templates',
        static_folder='../public'
    )

    env = Development
    if os.environ.get('APPLICATION_ENV', '') == 'Production':
        env = Production

    app.config.from_object(env)

    # Load config items into jinja settings
    for key, val in app.config.items():
        if key.startswith('JINJA'):
            setattr(app.jinja_env, key[6:].lower(), val)

    register_controllers(app)
    register_errorhandlers(app)
    register_extensions(app)

    return app


def register_controllers(app):
    import pkgutil
    from . import controllers

    for loader, name, ispkg in pkgutil.iter_modules(path=controllers.__path__):
        if not ispkg:
            __import__(controllers.__name__ + '.' + name)
            app.register_blueprint(getattr(controllers, name).blueprint)


def register_errorhandlers(app):
    def render_error(error):
        error = getattr(error, 'code', 500)
        return render_template('errors/{}.jinja'.format(error)), error

    for errcode in [403, 404, 500, 501]:
        app.errorhandler(errcode)(render_error)


def register_extensions(app):
    am.init_app(app)
