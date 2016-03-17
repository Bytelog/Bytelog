import os
import zopfli
import re

from csscompressor import compress
from slimit import minify
from glob2 import iglob
from io import BytesIO


# clear output directory
# get generator for directory
# compress file and compare with original
# save smaller version to output directory
# TODO: Only compress files which have changed
# TODO: Turn off gzipping in debug mode
# TODO: Turn off compression in debug mode
# TODO: Split into two stage: First minify, then compress.
# TODO: Compression stage should ensure timestamps match original file


class AssetManager:

    source = ''
    target = ''
    handlers = []

    def __init__(self, source, target):
        self.source = source
        self.target = target

    def register_handler(self, pattern, filters, actions):

        # TODO: Verify that pattern is a valid re.compile()
        self.handlers.append({
            'pattern': pattern,
            'filters': filters,
            'actions': actions
        })

    def _process(self):
        for source in iglob(os.path.join(self.source, '**')):
            path = os.path.relpath(source, self.source)
            try:
                item = next(handler for handler in self.handlers
                            if handler['pattern'].match(path))
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


def copyfilter(_in, out, path):
    out.write(_in.read())


def cssfilter(_in, out, path):
    out.write(compress(_in.read().decode()).encode())


def copyaction(_in, path):
    os.makedirs(os.path.split(path)[0], exist_ok=True)
    with open(path, 'wb') as f:
        f.write(_in.read())


def gzipaction(_in, path):
    source = _in.read()
    deflate = zopfli.ZopfliCompressor(zopfli.ZOPFLI_FORMAT_GZIP)
    compressed = (deflate.compress(source) + deflate.flush())

    print(path, len(compressed), len(source))
    if len(compressed) < len(source):
        os.makedirs(os.path.split(path)[0], exist_ok=True)
        with open(path + '.gz', 'wb') as f:
            f.write(compressed)


def pngaction(_in, path):
    source = _in.read()
    png = zopfli.ZopfliPNG()
    compressed = png.optimize(source)

    if len(compressed) < len(source):
        os.makedirs(os.path.split(path)[0], exist_ok=True)
        with open(path, 'wb') as f:
            f.write(compressed)


am = AssetManager('assets', 'public')
am.register_handler(re.compile('LICENSE.txt'), [copyfilter], [copyaction, gzipaction])
am.register_handler(re.compile('.*\.css'), [cssfilter], [copyaction, gzipaction])
am.register_handler(re.compile('.*\.png'), [], [pngaction])
am._process()

"""
for source in iglob('assets/images/**.png'):
    with open(source, 'rb') as f:
        data = f.read()

    png = zopfli.ZopfliPNG()
    target = png.optimize(data)
    deflate = zopfli.ZopfliCompressor(zopfli.ZOPFLI_FORMAT_GZIP)
    z = deflate.compress(target) + deflate.flush()

    if len(data) < len(target):
        target = data

    with open(os.path.join('public', source), 'wb') as f:
        f.write(target)

    with open(os.path.join('public', source + '.gz'), 'wb') as f:
        f.write(z)


for source in iglob('assets/scripts/**.js'):
    with open(source, 'r') as f:
        data = f.read()

    target = minify(data)
    deflate = zopfli.ZopfliCompressor(zopfli.ZOPFLI_FORMAT_GZIP)
    z = deflate.compress(target.encode()) + deflate.flush()

    if len(data) < len(target):
        target = data

    with open(os.path.join('public', source), 'w') as f:
        f.write(target)

    with open(os.path.join('public', source + '.gz'), 'wb') as f:
        f.write(z)
"""