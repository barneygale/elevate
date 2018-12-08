import sys

import elevate.elevate_util as elevate_util

# this is run at import time so as to prevent argument parsers before
#   the call to `elevate()` from breaking on our secret options
elevate_util._ELEVATE_GOT_ARGS = elevate_util._process_elevate_opts()


def elevate(show_console=True, graphical=True, restore_cwd=True):
    """
    Re-launch the current process with root/admin privileges

    When run as root, this function does nothing.

    When not run as root, this function replaces the current process (Linux,
    macOS) or creates a child process, waits, and exits (Windows).

    :param show_console: (Windows only) if True, show a new console for the
        child process. Ignored on Linux / macOS.
    :param graphical: (POSIX only) if True, attempt to use graphical
        programs (gksudo, etc). Ignored on Windows.
    :param restore_cwd: (POSIX only) if False, the calling process' previous
        working directory won't be restored after elevating.
        Currently ignored on Windows.
    """
    if sys.platform.startswith("win"):
        from elevate.windows import elevate
    else:
        from elevate.posix import elevate
    elevate(show_console, graphical, restore_cwd)
