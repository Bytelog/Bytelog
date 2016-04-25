import os
import signal

from .assets import AssetManager
from .config import Development
from .config import Production
from .document import Documents
from flask import Flask
from flask import render_template

am = AssetManager('assets', 'public')
documents = Documents('content', 'templates/cache')


# TODO: Move signal handlers into respective modules
def sig_handler(sig, frame):
    if sig == signal.SIGUSR1:
        # Rebuild Assets
        am._process()
    if sig == signal.SIGUSR2:
        # Reload Content
        documents.remove()
        documents.update()


def create_app():
    app = Flask(
        __name__.split('.')[0],
        template_folder='../templates',
        static_url_path=None,
        static_folder=None
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

    app.static_folder = '../public/'
    app.add_url_rule(app.config['STATIC_URL_PATH'] + '/<path:filename>',
                     endpoint='static',
                     view_func=app.send_static_file
                     )

    signal.signal(signal.SIGUSR1, sig_handler)
    signal.signal(signal.SIGUSR2, sig_handler)

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