import humanize

from .. import documents
from collections import OrderedDict
from datetime import datetime
from flask import Blueprint
from flask import render_template

blueprint = Blueprint('content', __name__)


@blueprint.context_processor
def inject_imports():
    return dict(datetime=datetime, humanize=humanize)

@blueprint.route('/', defaults={'page': 'index'})
@blueprint.route('/<page>')
def default(page):
    file = page + '.jinja'
    template = 'cache/' + file

    try:
        meta = reader.meta[file]
    except IndexError:
        meta = {}

    data = OrderedDict(sorted(reader.meta.items(), key=lambda x: x[1]['date']))
    return render_template(template, meta=meta, data=data)