from flask_assets import Bundle
from flask_assets import Environment
from csscompressor import compress

def cssmin(_in, out, **kw):
    out.write(compress(_in.read()))

def init_app(app):
    assets = Environment(app)

    styles = Bundle(
        '*.css',
        filters=cssmin,
        output='main.css',
    )

    scripts = Bundle(
        '*.js',
        filters='slimit',
        output='main.js'
    )

    assets.register('styles', styles)
    assets.register('scripts', scripts)

    # TODO: Disable auto building
    # TODO: Move this config to an environment file
    assets.load_path = ['assets/scripts', 'assets/styles']
    assets.config['SASS_STYLE'] = 'compressed'
    assets.url_expire = False
    assets.auto_build = True
