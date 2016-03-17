import os
import zopfli
import re

from csscompressor import compress
from slimit import minify
from glob2 import iglob
from io import BytesIO

# TODO: Only compress files which have changed
# TODO: Turn off gzipping in debug mode
# TODO: Turn off compression in debug mode
# TODO: Compression stage should ensure timestamps match original file


class AssetManager:

    source = ''
    target = ''
    handlers = []

    def __init__(self, source, target):
        self.source = source
        self.target = target

    def register(self, regex, filters, actions):
        self.handlers.append({
            'regex': regex,
            'filters': filters,
            'actions': actions
        })

    def _process(self):
        for source in iglob(os.path.join(self.source, '**')):
            path = os.path.relpath(source, self.source)
            try:
                item = next(x for x in self.handlers if x['regex'].match(path))
                _in = open(source, 'rb')
            except(OSError, StopIteration):
                continue

            for _filter in item['filters']:
                out = BytesIO()
                _filter(_in, out, path)
                _in = out
                _in.seek(0)

            for action in item['actions']:
                action(_in, os.path.join(self.target, path))
                _in.seek(0)


def cssmin(_in, out, path):
    out.write(compress(_in.read().decode()).encode())


def jsmin(_in, out, path):
    out.write(minify(_in.read().decode()).encode())


def copy(_in, path):
    os.makedirs(os.path.split(path)[0], exist_ok=True)
    with open(path, 'wb') as f:
        f.write(_in.read())


def deflate(_in, path):
    source = _in.read()
    deflate = zopfli.ZopfliCompressor(zopfli.ZOPFLI_FORMAT_GZIP)
    compressed = (deflate.compress(source) + deflate.flush())

    if len(compressed) < len(source):
        os.makedirs(os.path.split(path)[0], exist_ok=True)
        with open(path + '.gz', 'wb') as f:
            f.write(compressed)


def deflate_png(_in, path):
    source = _in.read()
    png = zopfli.ZopfliPNG()
    compressed = png.optimize(source)
    os.makedirs(os.path.split(path)[0], exist_ok=True)
    target = compressed if len(compressed) < len(source) else source

    with open(path, 'wb') as f:
        f.write(target)


am = AssetManager('assets', 'public')
am.register(re.compile('.*\.css'), [cssmin], [copy, deflate])
am.register(re.compile('.*\.js'), [jsmin], [copy, deflate])
am.register(re.compile('.*\.png'), [], [deflate_png])
am.register(re.compile('.*'), [], [copy, deflate])
am._process()
