#!/usr/bin/env python3

from argparse import ArgumentParser
from os import path

from PIL import Image
from requests import Session


def _glue_url(*parts):
    # append trailing slash by ending with an empty string (for peter's sake :))
    return path.join(*(str(part) for part in parts), '')


class LedderClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.session = Session()

    def put_led(self, loc, color):
        x, y = loc
        self.session.put(_glue_url(self.endpoint, 'leds', x, y), json=list(color))


def to_pixels(buffer, target_size):
    image = Image.open(buffer)
    # TODO: preserve aspect ratio, insert empty lines as to center
    image = image.resize(target_size)
    image.show()

    data = image.getdata()
    # strip anything outside rgb
    return tuple((r, g, b) for r, g, b, *_ in data)


def main(args):
    with open(args.image, 'rb') as image:
        pixels = to_pixels(image, (12, 10))

    client = LedderClient(args.endpoint)
    for idx, pixel in enumerate(pixels):
        x = idx % 12
        y = idx // 10
        print('setting pixel ({}, {}) to {}'.format(x, y, pixel))
        client.put_led((x, y), pixel)


if __name__ == '__main__':
    parser = ArgumentParser(description='render picture file to tuintrip led matrix')
    parser.add_argument('image')
    parser.add_argument('-e', '--endpoint', default='http://192.168.1.25:5000')

    args = parser.parse_args()
    main(args)
