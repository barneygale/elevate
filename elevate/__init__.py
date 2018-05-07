import sys


def elevate(show_console=True, graphical=True):
    """
    Re-launch the current process with root/admin privileges

    When run as root, this function does nothing.

    When not run as root, this function replaces the current process (Linux,
    macOS) or creates a child process, waits, and exits (Windows).

    :param show_console: (Windows only) if True, show a new console for the
        child process. Ignored on Linux / macOS.
    :param graphical: (Linux / macOS only) if True, attempt to use graphical
        programs (gksudo, etc). Ignored on Windows.
    """
    if sys.platform.startswith("win"):
        from elevate.windows import elevate
    else:
        from elevate.posix import elevate
    elevate(show_console, graphical)

