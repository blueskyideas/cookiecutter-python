#!/usr/bin/env python3.6

'''
Set up application for the first time after cloning, or set it
back to the initial first unused state.


Part of the 'Scripts to Rule them All' suite of scripts to provide a consistent
developer experience for working on our repos

https://githubengineering.com/scripts-to-rule-them-all/

'''

import argparse
import logging
import sys
import os
import site
import shutil

import common
import bootstrap

_LOGGER = logging.getLogger("script.setup")


def run(*, verbose=False):
    common.run(_LOGGER, verbose=verbose)
    creds_file = os.path.abspath(creds_file)

    bootstrap.run(verbose=verbose)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(
        description=("Set up application for the first time after cloning, or set it "
                     "back to the initial first unused state")
    )
    parser.add_argument("-v",action="store_true", help="Verbose output")
    parser.add_argument("creds_file",
        help=(
            "path to existing creds file"
            )
    )

    args = parser.parse_args()
    print(args)

    common.setup_parent_loggers()
    run(verbose=args.v)