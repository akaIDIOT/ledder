#!/usr/bin/env python3

from argparse import ArgumentParser


def main(args):
    pass


if __name__ == '__main__':
    parser = ArgumentParser(description='render picture file to tuintrip led matrix')
    parser.add_argument('image')

    args = parser.parse_args()
    main(args)
