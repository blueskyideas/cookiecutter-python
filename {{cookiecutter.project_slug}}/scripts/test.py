#!/usr/bin/env python3.6

'''
Run the test suite.

Part of the Scripts to Rule them All suite of scripts to provide a consistent
developer experience for working on our repos

https://githubengineering.com/scripts-to-rule-them-all/

'''

import argparse
import logging
import os
import subprocess

import common
import bootstrap

_LOGGER = logging.getLogger("script.test")

def run(*, verbose=False, sqlite_echo=False, skip_bootstrap=False, pytest_options=None):
    common.run(_LOGGER, verbose=verbose)
    os.environ['PIPENV_VENV_IN_PROJECT'] = "1"
    
    if sqlite_echo:
        os.environ['SQLITE_ECHO'] = "y"
    else:
        os.environ['SQLITE_ECHO'] = "n"

    os.environ['PYTEST_ADDOPTS']="--color=yes"

    if not skip_bootstrap:
        bootstrap.run(verbose=verbose)

    cmd = ["pipenv", "run","pytest"]
    if pytest_options:
        cmd.append(pytest_options)

    common.run_cmd(_LOGGER, cmd, raw_log=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(
        description="Run the test suite"
    )
    parser.add_argument("-v",action="store_true", help="Verbose output")
    parser.add_argument("--sqlite_echo",action="store_true", help="Show sqlite debug messages")
    parser.add_argument("--skip_bootstrap",action="store_true", help="skip bootstrapping before running tests")
    parser.add_argument("--pytest",help="extra pytest options")

    args = parser.parse_args()
    print(args)

    common.setup_parent_loggers()
    run(
        verbose=args.v, 
        sqlite_echo=args.sqlite_echo,
        skip_bootstrap=args.skip_bootstrap,
        pytest_options=args.pytest
    )


