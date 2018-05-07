import sys


def elevate():
    """
    Re-launch the current process with root/admin privileges

    When run as root, this function does nothing.

    When not run as root, this function replaces the current process (Linux,
    macOS) or creates a child process, waits, and exits (Windows).
    """

    if sys.platform.startswith("win"):
        from elevate.windows import elevate
    else:
        from elevate.posix import elevate
    elevate()

