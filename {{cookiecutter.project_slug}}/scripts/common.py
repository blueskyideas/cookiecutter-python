#!/usr/bin/env python3.6

'''
File that contains all the common code for the scripts


Part of the 'Scripts to Rule them All' suite of scripts to provide a consistent
developer experience for working on our repos

https://githubengineering.com/scripts-to-rule-them-all/

'''

import argparse
import logging
import subprocess
import os
import sys

def run_cmd(logger, cmd, expect_error=False, raw_log=False):
    logger.debug("+{}".format(" ".join(cmd)))

    if raw_log:
        #inherit stdout, stderr from parent
        proc = subprocess.Popen(
            cmd,
            bufsize=0,
        )
    else:
        proc = subprocess.Popen(
            cmd,
            bufsize=0,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,

        )

        stdout_lines = []
        for line in iter(proc.stdout.readline, b''):
            stdout_str = line.decode("utf-8") #has new line at the end
            stdout_lines.append(stdout_str)

            if stdout_str[-1] == "\n":
                logger.debug(stdout_str[:-1])
            else:
                logger.debug(stdout_str)

    proc.wait()

    if proc.returncode == 0:
        if expect_error:
            raise ValueError("return code shouldnt be zero")
        else:
            if not raw_log:
                return "".join(stdout_lines)
            else:
                return
    else:
        if expect_error:
            if not raw_log:
                return "".join(stdout_lines)
            else:
                return
        else:
            raise ValueError("non zero return code {}".format(proc.returncode))



def setup_parent_loggers():
    #root logger tracks everything but has no handler
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    #script logger tracks everything and has a handler. Up to child loggers as to
    #whether their messages get sent to it.
    script_logger = logging.getLogger("script")
    script_logger.setLevel(logging.DEBUG)

    hdlr = logging.StreamHandler()
    fmt = logging.Formatter(
        "%(asctime)s: %(levelname)s: %(name)s (%(process)d): %(message)s"
    )

    hdlr.setFormatter(fmt)

    script_logger.addHandler(hdlr)
    script_logger.propagate = True


def bootstrap_color_logging():

    script_logger = logging.getLogger("script")
    script_logger.removeHandler(script_logger.handlers[0])

    import colorlog

    fmt="%(asctime)s: %(levelname)s: %(name)s (%(process)d): %(message)s"
    colorfmt = "%(log_color)s{}%(reset)s".format(fmt)
    formatter_obj = colorlog.ColoredFormatter(
        colorfmt,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        }
    )
    hdlr.setFormatter(formatter_obj)

    script_logger.addHandler(hdlr)



def make_dir(logger, out_dir):
    logger.debug("creating directory if it doesn't exist: {}".format(out_dir))
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

def setup_logger(logger, lvl):
    logger.setLevel(lvl)
    logger.propagate = True

def run(logger, *, verbose=False):
    if verbose:
        setup_logger(logger, logging.DEBUG)
    else:
        setup_logger(logger, logging.INFO)








#The Following code makes the virtual env relocatable by fixing up script shebangs
#and .pth and .egg-links
#Taken from https://github.com/pypa/virtualenv/blob/master/virtualenv.py

def path_locations(home_dir):
    """Return the path locations for the environment (where libraries are,
    where scripts go, etc)"""
    home_dir = os.path.abspath(home_dir)
    abiflags = getattr(sys, 'abiflags', '')
    py_version = 'python%s.%s' % (sys.version_info[0], sys.version_info[1])

    lib_dir = os.path.join(home_dir, 'lib', py_version)
    inc_dir = os.path.join(home_dir, 'include', py_version + abiflags)
    bin_dir = os.path.join(home_dir, 'bin')
    return home_dir, lib_dir, inc_dir, bin_dir



def make_environment_relocatable(logger, home_dir):
    """
    Makes the already-existing environment use relative paths, and takes out
    the #!-based environment selection in scripts.
    """

    home_dir, lib_dir, inc_dir, bin_dir = path_locations(home_dir)

    #JR: added site packages to sys.path so that egg-links and pth files can be made relative
    site_packages_dir = os.path.join(lib_dir,"site-packages")
    sys.path.insert(0, site_packages_dir)

    activate_this = os.path.join(bin_dir, 'activate_this.py')
    if not os.path.exists(activate_this):
        logger.critical(
            'The environment doesn\'t have a file %s -- please re-run virtualenv '
            'on this environment to update it' % activate_this)
    fixup_scripts(logger, home_dir, bin_dir)
    fixup_pth_and_egg_link(logger, home_dir)
    ## FIXME: need to fix up distutils.cfg

OK_ABS_SCRIPTS = ['python', 'python%s' % sys.version[:3],
                  'activate', 'activate.bat', 'activate_this.py',
                  'activate.fish', 'activate.csh']

def fixup_scripts(logger, home_dir, bin_dir):
    new_shebang_args = ('/usr/bin/env', sys.version[:3], '')

    # This is what we expect at the top of scripts:
    shebang = '#!%s' % os.path.normcase(os.path.join(
        os.path.abspath(bin_dir), 'python%s' % new_shebang_args[2]))
    # This is what we'll put:
    new_shebang = '#!%s python%s%s' % new_shebang_args

    for filename in os.listdir(bin_dir):
        filename = os.path.join(bin_dir, filename)
        if not os.path.isfile(filename):
            # ignore subdirs, e.g. .svn ones.
            continue
        lines = None
        with open(filename, 'rb') as f:
            try:
                lines = f.read().decode('utf-8').splitlines()
            except UnicodeDecodeError:
                # This is probably a binary program instead
                # of a script, so just ignore it.
                continue
        if not lines:
            logger.warn('Script %s is an empty file' % filename)
            continue

        old_shebang = lines[0].strip()
        old_shebang = old_shebang[0:2] + os.path.normcase(old_shebang[2:])

        if not old_shebang.startswith(shebang):
            if os.path.basename(filename) in OK_ABS_SCRIPTS:
                logger.debug('Cannot make script %s relative' % filename)
            elif lines[0].strip() == new_shebang:
                logger.info('Script %s has already been made relative' % filename)
            else:
                logger.warn('Script %s cannot be made relative (it\'s not a normal script that starts with %s)'
                            % (filename, shebang))
            continue
        logger.info('Making script %s relative' % filename)
        script = relative_script([new_shebang] + lines[1:])
        with open(filename, 'wb') as f:
            f.write('\n'.join(script).encode('utf-8'))


def relative_script(lines):
    "Return a script that'll work in a relocatable environment."
    activate = "import os; activate_this=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'activate_this.py'); exec(compile(open(activate_this).read(), activate_this, 'exec'), dict(__file__=activate_this)); del os, activate_this"
    # Find the last future statement in the script. If we insert the activation
    # line before a future statement, Python will raise a SyntaxError.
    activate_at = None
    for idx, line in reversed(list(enumerate(lines))):
        if line.split()[:3] == ['from', '__future__', 'import']:
            activate_at = idx + 1
            break
    if activate_at is None:
        # Activate after the shebang.
        activate_at = 1
    return lines[:activate_at] + ['', activate, ''] + lines[activate_at:]

def fixup_pth_and_egg_link(logger, home_dir, sys_path=None):
    """Makes .pth and .egg-link files use relative paths"""
    home_dir = os.path.normcase(os.path.abspath(home_dir))
    if sys_path is None:
        sys_path = sys.path
    for path in sys_path:
        if not path:
            path = '.'
        if not os.path.isdir(path):
            continue
        path = os.path.normcase(os.path.abspath(path))
        if not path.startswith(home_dir):
            logger.debug('Skipping system (non-environment) directory %s' % path)
            continue
        for filename in os.listdir(path):
            filename = os.path.join(path, filename)
            if filename.endswith('.pth'):
                if not os.access(filename, os.W_OK):
                    logger.warn('Cannot write .pth file %s, skipping' % filename)
                else:
                    fixup_pth_file(logger, filename)
            if filename.endswith('.egg-link'):
                if not os.access(filename, os.W_OK):
                    logger.warn('Cannot write .egg-link file %s, skipping' % filename)
                else:
                    fixup_egg_link(logger, filename)

def fixup_pth_file(logger, filename):
    lines = []
    prev_lines = []
    with open(filename) as f:
        prev_lines = f.readlines()
    for line in prev_lines:
        line = line.strip()
        if (not line or line.startswith('#') or line.startswith('import ')
            or os.path.abspath(line) != line):
            lines.append(line)
        else:
            new_value = make_relative_path(filename, line)
            if line != new_value:
                logger.debug('Rewriting path %s as %s (in %s)' % (line, new_value, filename))
            lines.append(new_value)
    if lines == prev_lines:
        logger.info('No changes to .pth file %s' % filename)
        return
    logger.info('Making paths in .pth file %s relative' % filename)
    with open(filename, 'w') as f:
        f.write('\n'.join(lines) + '\n')

def fixup_egg_link(logger, filename):
    with open(filename) as f:
        link = f.readline().strip()
    if os.path.abspath(link) != link:
        logger.debug('Link in %s already relative' % filename)
        return
    new_link = make_relative_path(filename, link)
    logger.info('Rewriting link %s in %s as %s' % (link, filename, new_link))
    with open(filename, 'w') as f:
        f.write(new_link)

def make_relative_path(source, dest, dest_is_directory=True):
    """
    Make a filename relative, where the filename is dest, and it is
    being referred to from the filename source.
        >>> make_relative_path('/usr/share/something/a-file.pth',
        ...                    '/usr/share/another-place/src/Directory')
        '../another-place/src/Directory'
        >>> make_relative_path('/usr/share/something/a-file.pth',
        ...                    '/home/user/src/Directory')
        '../../../home/user/src/Directory'
        >>> make_relative_path('/usr/share/a-file.pth', '/usr/share/')
        './'
    """
    source = os.path.dirname(source)
    if not dest_is_directory:
        dest_filename = os.path.basename(dest)
        dest = os.path.dirname(dest)
    dest = os.path.normpath(os.path.abspath(dest))
    source = os.path.normpath(os.path.abspath(source))
    dest_parts = dest.strip(os.path.sep).split(os.path.sep)
    source_parts = source.strip(os.path.sep).split(os.path.sep)
    while dest_parts and source_parts and dest_parts[0] == source_parts[0]:
        dest_parts.pop(0)
        source_parts.pop(0)
    full_parts = ['..']*len(source_parts) + dest_parts
    if not dest_is_directory:
        full_parts.append(dest_filename)
    if not full_parts:
        # Special case for the current directory (otherwise it'd be '')
        return './'
    return os.path.sep.join(full_parts)
