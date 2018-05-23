#!/usr/bin/env python3.6

'''
Launch the application and any extra required processes
locally

Part of the 'Scripts to Rule them All' suite of scripts to provide a consistent
developer experience for working on our repos

https://githubengineering.com/scripts-to-rule-them-all/

'''

import argparse
import logging
import os

import common

_LOGGER = logging.getLogger("script.server")

def run(*, verbose=False):
    common.run(_LOGGER, verbose=verbose)
    _LOGGER.info("This script currently does nothing")




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(
        description=("Launch the application and any extra required processes locally")
    )
    parser.add_argument("-v",action="store_true", help="Verbose output")

    args = parser.parse_args()
    print(args)

    common.setup_parent_loggers()
    run(verbose=args.v)