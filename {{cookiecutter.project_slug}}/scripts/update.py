#!/usr/bin/env python3.6

'''
Update application to run for its current checkout.

Part of the 'Scripts to Rule them All' suite of scripts to provide a consistent
developer experience for working on our repos

https://githubengineering.com/scripts-to-rule-them-all/

'''

import argparse
import logging
import os

import common
import bootstrap

_LOGGER = logging.getLogger("script.update")

def run(*, verbose=False):
    common.run(_LOGGER, verbose=verbose)
    bootstrap.run(verbose=verbose)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(
        description=("Update application to run for its current checkout.")
    )
    parser.add_argument("-v",action="store_true", help="Verbose output")

    args = parser.parse_args()
    print(args)

    common.setup_parent_loggers()
    run(verbose=args.v)