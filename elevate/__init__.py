import argparse
import os
import sys


cwd_argument = "--elevate-cwd"


def elevate(show_console=True, graphical=True, make_absolute=True,
            preserve_cwd=False):
    """
    Re-launch the current process with root/admin privileges

    When run as root, this function does nothing.

    When not run as root, this function replaces the current process (Linux,
    macOS) or creates a child process, waits, and exits (Windows).

    :param show_console: (Windows only) if True, show a new console for the
        child process. Ignored on Linux / macOS.
    :param graphical: (Linux / macOS only) if True, attempt to use graphical
        programs (gksudo, etc). Ignored on Windows.
    :param make_absolute: if True, any command-line arguments that exist as
        files on disk will be transformed into absolute paths
    :param preserve_cwd: if True, the working directory will be preserved by
        passing and later parsing a command-line argument. Enabling this option
        also prevents a possible infinite loop on Windows.
    """

    args = sys.argv[:]

    if make_absolute:
        args = [os.path.abspath(arg)
                if os.path.exists(arg) and not os.path.isabs(arg)
                else arg
                for arg in args]

    if preserve_cwd:
        if cwd_argument in args:
            os.chdir(args[1 + args.index(cwd_argument)])
            return
        else:
            args += [cwd_argument, os.getcwd()]


    if sys.platform.startswith("win"):
        from elevate.windows import elevate
    else:
        from elevate.posix import elevate
    elevate(show_console, graphical, args)


def add_parser_argument(parser):
    """
    Adds a dummy ``--elevate-cwd`` argument to the given
    ``argparse.ArgumentParser`` object.
    """

    parser.add_argument(cwd_argument, help=argparse.SUPRESS)
