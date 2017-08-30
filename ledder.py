#!/usr/bin/env python3

from argparse import ArgumentParser

from PIL import Image


def to_pixels(buffer, target_size):
    image = Image.open(buffer)
    # TODO: preserve aspect ratio, insert empty lines as to center
    image = image.resize(target_size)

    data = image.getdata()
    # strip anything outside rgb
    return tuple((r, g, b) for r, g, b, *_ in data)


def main(args):
    with open(args.image, 'rb') as image:
        pixels = to_pixels(image, (12, 10))


if __name__ == '__main__':
    parser = ArgumentParser(description='render picture file to tuintrip led matrix')
    parser.add_argument('image')

    args = parser.parse_args()
    main(args)
