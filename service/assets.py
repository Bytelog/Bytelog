import os
import zopfli
import re

from csscompressor import compress
from slimit import minify
from glob2 import iglob
from io import BytesIO

# TODO: Turn off gzipping in debug mode
# TODO: Turn off compression in debug mode
# TODO: Add logging


class AssetManager:

    source = ''
    target = ''
    handlers = []
    timestamp = 0

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
        for source_path in iglob(os.path.join(self.source, '**')):
            path = os.path.relpath(source_path, self.source)
            target_path = os.path.join(self.target, path)

            try:
                target_time = os.path.getmtime(target_path)
            except OSError:
                target_time = 0

            try:
                self.timestamp = os.path.getmtime(source_path)
                if self.timestamp == target_time:
                    raise ValueError
                item = next(x for x in self.handlers if x['regex'].match(path))
                _in = open(source_path, 'rb')
            except(OSError, StopIteration, ValueError):
                continue

            for _filter in item['filters']:
                out = BytesIO()
                _filter(_in, out, path)
                _in = out
                _in.seek(0)

            for action in item['actions']:
                out = BytesIO()
                target_path = action(_in, out, target_path)
                _in.seek(0)
                out.seek(0)

                if target_path:
                    self._write(out, target_path)

            _in.close()

    def _write(self, data, path):
        os.makedirs(os.path.split(path)[0], exist_ok=True)

        with open(path, 'wb') as f:
            f.write(data.read())

        os.utime(path, (self.timestamp, self.timestamp))

    def init_app(self, app):
        self.register(re.compile('.*\.css'), [cssmin], [copy, deflate])
        self.register(re.compile('.*\.js'), [jsmin], [copy, deflate])
        self.register(re.compile('.*\.png'), [], [deflate_png])
        self.register(re.compile('.*'), [], [copy, deflate])
        self._process()


def cssmin(_in, out, source_path):
    out.write(compress(_in.read().decode()).encode())


def jsmin(_in, out, source_path):
    out.write(minify(_in.read().decode()).encode())


def copy(_in, out, target_path):
    out.write(_in.read())
    return target_path


def deflate(_in, out, target_path):
    source = _in.read()
    deflate = zopfli.ZopfliCompressor(zopfli.ZOPFLI_FORMAT_GZIP)
    compressed = (deflate.compress(source) + deflate.flush())

    if len(compressed) < len(source):
        out.write(compressed)
        return target_path + '.gz'


def deflate_png(_in, out, target_path):
    source = _in.read()
    png = zopfli.ZopfliPNG()
    compressed = png.optimize(source)
    data = compressed if len(compressed) < len(source) else source
    out.write(data)
    return target_path
