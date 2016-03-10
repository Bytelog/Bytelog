import os
import zopfli

from csscompressor import compress
from slimit import minify
from glob2 import iglob


# clear output directory
# get generator for directory
# compress file and compare with original
# save smaller version to output directory
# TODO: Add support for bundling
# TODO: Turn off gzipping in debug mode
# TODO: Turn off compression in debug mode
# TODO: Split into two stage: First minify, then compress.
# TODO: Compression stage should ensure timestamps match original file

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


for source in iglob('assets/styles/**.css'):
    with open(source, 'r') as f:
        data = f.read()

    target = compress(data)
    deflate = zopfli.ZopfliCompressor(zopfli.ZOPFLI_FORMAT_GZIP)
    z = deflate.compress(target.encode()) + deflate.flush()

    if len(data) < len(target):
        target = data

    with open(os.path.join('public', source), 'w') as f:
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
