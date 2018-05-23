#!/usr/bin/env python3.6

'''
Resolve all dependencies that the application requires to run. Called by other scripts.

Part of the 'Scripts to Rule them All' suite of scripts to provide a consistent
developer experience for working on our repos

https://githubengineering.com/scripts-to-rule-them-all/

'''

import argparse
import logging
import os

import common

_LOGGER = logging.getLogger("script.bootstrap")

def run(*, verbose=False):
    common.run(_LOGGER, verbose=verbose)
    os.environ['PIPENV_VENV_IN_PROJECT'] = "1"
    
    common.run_cmd(_LOGGER, ["pipenv", "uninstall", "--all"])
    common.run_cmd(_LOGGER, ["pipenv", "install", "--dev"])
    common.run_cmd(_LOGGER, ["pipenv", "--venv"])




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(
        description="Resolve all dependencies that the application requires to run"
    )
    parser.add_argument("-v",action="store_true", help="Verbose output")

    args = parser.parse_args()
    print(args)

    common.setup_parent_loggers()
    run(verbose=args.v)