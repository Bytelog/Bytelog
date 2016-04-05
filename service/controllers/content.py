import humanize

from .. import documents
from datetime import datetime
from flask import Blueprint
from flask import render_template
from flask import request
from htmlmin.main import Minifier

blueprint = Blueprint('content', __name__)

minifier = Minifier(
        remove_comments=True,
        remove_empty_space=True,
        reduce_boolean_attributes=True,
    )


@blueprint.context_processor
def inject_imports():
    return dict(datetime=datetime, humanize=humanize)


@blueprint.after_request
def response_minify(response):
    response.set_data(minifier.minify(response.get_data(as_text=True)))
    return response


@blueprint.route('/', defaults={'page': 'index'})
@blueprint.route('/<path:page>')
def default(page):
    file = page + '.jinja'
    template = 'cache/' + file

    try:
        meta = documents.meta[page]
    except IndexError:
        meta = {}

    data = documents.meta
    return render_template(template, meta=meta, data=data, request=request)
