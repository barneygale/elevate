Elevate: Request root privileges
================================

Elevate is a small Python library that re-launches the current process with
root/admin privileges using one of the following mechanisms:

- UAC (Windows)
- AppleScript (macOS)
- ``pkexec``, ``gksudo`` or ``kdesudo`` (Linux)
- ``sudo`` (Linux, macOS)

Usage
-----

To use, call ``elevate.elevate()`` early in your script. When run as root this
function does nothing. When not run as root, this function replaces the current
process (Linux, macOS) or creates a new process, waits, and exits (Windows).
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

On Windows, the new process's standard streams are not attached to the parent,
which is an inherent limitation of UAC. By default the new process runs in a
new console window. To suppress this window, use
``elevate(show_console=False)``.

On Linux and macOS, graphical prompts are tried before ``sudo`` by default. To
prevent graphical prompts, use ``elevate(graphical=False)``.
