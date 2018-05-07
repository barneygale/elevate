Elevate: Request root privileges
================================

Elevate is a small Python library that re-launches the current process with
root/admin privileges using one of the following mechanisms:

- UAC (Windows)
- AppleScript (macOS)
- ``gksudo`` (Linux)
- ``kdesudo`` (Linux)
- ``sudo`` (Linux, macOS)

To use, call ``elevate.elevate()`` early in your script. When run as root this
function does nothing. When not run as root, this function replaces the current
process (Linux, macOS) or creates a child process, waits, and exits (Windows).
Consider the following example:

.. code-block:: python

    import os
    from elevate import elevate

    def is_root():
        return os.getuid() == 0

    print("before ", is_root())
    elevate()
    print("after ", is_root())

This prints::

    before False
    before True
    after True
