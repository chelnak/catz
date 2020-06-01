#!/usr/bin/env python3

import sys
import configargparse


def get_args():

    parser = configargparse.ArgParser()
    parser.add("filename",
               help='Path to the file that will be loaded')

    args = parser.parse_args()

    if args.filename is None:
        print("Required argument filename is missing")
        print(parser.print_help())
        sys.exit(1)

    return args
