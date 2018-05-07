Elevate: Request root privileges
================================

Elevate is a small Python library that re-launches the current process with
root/admin privileges using one of the following mechanisms:

- UAC (Windows)
- AppleScript (macOS)
- ``gksudo`` (Linux)
- ``kdesudo`` (Linux)
- ``sudo`` (Linux, macOS)

To use, call ``elevate.elevate()`` early in your script. When not run as root,
this function replaces the current process (Linux, macOS) or creates a child
process, waits, and exits (Windows).

To illustrate, consider the following example::

    import os
    from elevate import elevate

    print("# before ", os.getuid())
    elevate()
    print("# after ", os.getuid())

This prints::

    # before 1000
    # before 0
    # after 0
