#!/usr/bin/env python3

from argparse import ArgumentParser
from os import path

from PIL import Image
from requests import Session


def _glue_url(*parts):
    # append an empty string to make the url end in a /
    # (seems flask breaks things if we don't)
    return path.join(*(str(part) for part in parts), '')


class LedderClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.session = Session()

    def put_all(self, leds):
        response = self.session.put(_glue_url(self.endpoint, 'ledstrip'), json=leds)
        assert response.status_code == 200, 'unexpected response code: {}: {}'.format(
            response.status_code,
            response.reason
        )


def rows(pixels, width):
    for start in range(0, len(pixels), width):
        yield pixels[start:start + width]


def to_pixels(buffer, target_size):
    # load image, create a thumbnail from it
    image = Image.open(buffer)
    image.thumbnail(target_size)

    target_width, target_height = target_size
    # image is to be centered, calculate x and y offsets
    target_x = (target_width - image.width) // 2
    target_y = (target_height - image.height) // 2

    # create new image of target size
    result = Image.new('RGB', target_size)
    # paste the thumbnail into it, at an offset
    result.paste(image, (target_x, target_y))

    # strip anything outside rgb
    return tuple((r, g, b) for r, g, b, *_ in result.getdata())


def main(args):
    with open(args.image, 'rb') as image:
        pixels = to_pixels(image, (args.width, args.height))
        assert len(pixels) == args.width * args.height, 'refusing to upscale images'

    client = LedderClient(args.endpoint)
    # construct data, list of dicts with an rgb value for an x/y coord
    leds = [{'x': idx % args.width,
             'y': idx // args.width,
             'rgb': rgb}
            for idx, rgb in enumerate(pixels)]
    # push all led data to remote
    client.put_all(leds)


if __name__ == '__main__':
    parser = ArgumentParser(description='render picture file to tuintrip led matrix')
    parser.add_argument('image')
    parser.add_argument('--endpoint', default='http://192.168.1.25:5000')
    parser.add_argument('--width', type=int, default=12)
    parser.add_argument('--height', type=int, default=10)

    args = parser.parse_args()
    main(args)
