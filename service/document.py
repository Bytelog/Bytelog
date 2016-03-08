import os
import re
import dateutil.parser
import textwrap
from datetime import datetime
from flask.ext.misaka import markdown
from glob2 import glob
from logging import error
from logging import info
from titlecase import titlecase


class Documents():

    meta = {}
    source = ''
    target = ''

    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.remove()
        self.update()

    def _parse_metadata(self, lines):
        meta = {}

        for key, line in enumerate(lines):
            result = re.match('^(\w*)[ \t]*:[ \t]*(.*)?[ \t]*$', line)

            if not result:
                break

            meta[result.group(1).lower()] = result.group(2)

        return (self._normal_metadata(meta), ''.join(lines[key:]))

    def _normal_metadata(self, meta):

        def check(key):
            return key in meta and meta[key]

        def clean(key, action, default):
            meta[key] = action(meta[key]) if check(key) else default()

        def required():
            raise KeyError("Missing required value.")

        try:
            clean('title', titlecase, required)
            clean('author', titlecase, lambda: None)
            clean('date', dateutil.parser.parse, required)
            clean('keywords', lambda x: x.lower().split(), lambda: [])
            clean('template', lambda x: x, lambda: 'default')
            clean('prev', lambda x: x, lambda: None)
            clean('next', lambda x: x, lambda: None)
        except(KeyError, ValueError, OverflowError) as e:
            raise ValueError("Unable to parse meta information: {}".format(e))

        return meta

    def _embed_templating(self, html, metadata):
        return textwrap.dedent('''\
            {{% extends '{template}.jinja' %}}
            {{% block content %}}
            {content}{{% endblock %}}
            ''').format(content=html, template=metadata['template'])

    def _build(self, path):
        # TODO: Allow other file types
        if not path.endswith('.md'):
            raise ValueError('Skipping non-markdown file.')

        with open(path) as f:
            meta, content = self._parse_metadata(f.readlines())

        if datetime.now() < meta['date']:
            raise ValueError("Skipping until published")

        # TODO: Pass config[markdown] to the markdown parser
        return (meta, self._embed_templating(markdown(content), meta))

    # TODO: Restrict to not go up directories
    def _trie_glob(self, path):
        glob_path = os.path.join(os.path.split(path)[0], '**')
        return [e for e in glob(glob_path) if e.startswith(path)]

    def update(self, path=''):
        for item in self._trie_glob(os.path.join(self.source, path)):
            try:
                rel = os.path.splitext(os.path.relpath(item, self.source))[0]
                target = os.path.join(self.target, rel)
                if os.path.isdir(item):
                    os.makedirs(target, exist_ok=True)
                else:
                    meta, html = self._build(item)
                    with open(target + '.jinja', 'w+') as f:
                        f.write(html)
                        self.meta[rel] = meta
            except ValueError as e:
                info("{}: {}".format(rel, e))
            except OSError as e:
                error("{}: {}".format(rel, e))

    def remove(self, path=''):
        for item in reversed(self._trie_glob(os.path.join(self.target, path))):
            try:
                os.remove(item) if os.path.isfile(item) else os.rmdir(item)
            except OSError as e:
                error("{}: {}".format(item, e))
            self.meta.pop(os.path.splitext(os.path.relpath(item, self.target))[0], None)
