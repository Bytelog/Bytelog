from . import assets
from .document import Documents
from flask import Flask
from flask import render_template
from flask.ext.misaka import Misaka


md = Misaka()
documents = Documents('content', 'assets/templates/cache')


def create_app():
    app = Flask(
        __name__.split('.')[0],
        static_url_path='/static',
        static_folder='../public',
        template_folder='../assets/templates'
    )

    register_controllers(app)
    register_errorhandlers(app)
    register_extensions(app)

    # TODO: Remove after flask-assets > 0.11
    app.jinja_env.assets_environment.environment = app.jinja_env.assets_environment

    # TODO: Move to environment config
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True
    app.debug = True

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
    md.init_app(app)
    assets.init_app(app)
