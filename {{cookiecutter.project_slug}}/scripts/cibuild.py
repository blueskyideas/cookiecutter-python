#!/usr/bin/env python3.6

'''
Setup environment for CI to run tests. This is primarily
designed to run on the continuous integration server.

Part of the 'Scripts to Rule them All' suite of scripts to provide a consistent
developer experience for working on our repos

https://githubengineering.com/scripts-to-rule-them-all/

'''

import argparse
import logging
import os

import common

_LOGGER = logging.getLogger("script.cibuild")

def run(*, verbose=False):
    common.run(_LOGGER, verbose=verbose)
    _LOGGER.debug("This script currently does nothing")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(
        description=("Setup environment for CI to run tests. This is primarily "
                     "designed to run on the continuous integration server.")
    )
    parser.add_argument("-v",action="store_true", help="Verbose output")

    args = parser.parse_args()
    print(args)

    common.setup_parent_loggers()
    run(verbose=args.v)