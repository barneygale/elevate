import sys

# two parts of the prefix of a special elevate command-line option
_OPT_PREFIX = ("--_", "with-elevate-")
# preserve the command-line arguments to elevate()
_ELEVATE_GOT_ARGS = dict()


def _process_elevate_opts():
    """
        Arguments:  none
        Returns:    dict() mapping elevate command-line options to their values
                    for clarity and disambiguation the `with-elevate-` prefixes
                        are retained
        Throws:     No
        Effects:    Changes sys.argv, removing options specific to elevate

        Simple option filter to remove and remember --_with-elevate-* options,
            which would break argument parsers that appear before the
            invocation of `elevate.elevate()`

        These options allow elevate to give data to the elevated process it
            will spawn.

        This function reads and changes the entire argument list, and so
            elevate's special options are not positional.

        Calling this function again after the first time will have no effect.

        Use _elevate_util._get_opt(opts, name) to get an option from this
            dictionary.
    """
    opttest = lambda x, m=True: m == all(
        ["=" in x, x.startswith( "".join(_OPT_PREFIX) )]
    )

    # copy sys.argv (compatibility)
    old_argv = list(sys.argv)
    # prevent user code from seeing elevate's options
    sys.argv = list(filter(lambda x: opttest(x, False), old_argv))
    return dict(map(
        lambda y: y.split("_")[1].split("="), filter(opttest, old_argv)
    ))


def _get_opt(opts, name):
    """
        Arguments:  opts (a dictionary of options and values, like returned
                        from _process_elevate_opts)
                    name (the base name of the option to get, without its
                        with-elevate prefix)
        Returns:    The value of the option, which might be boolean, or False
                        if the option wasn't specified
        Throws:     No
        Effects:    none

        Safe/checked way to get an elevate option from a _process_elevate_opts
            dictionary.
    """
    return opts.get(_OPT_PREFIX[1] + name, False)


def _make_opt(name, param):
    """
        Arguments:  name (the base name of the option, without its
                        'with-elevate-' prefix)
                    param (the string value to specify as the parameter for the
                        option)
        Returns:    The string name of the command-line option, to be specified
                        in the elevated process.
        Throws:     No
        Effects:    none

        Format the special elevate option with the name `name` and the
            parameter `param`, so that a process can be launched with it.
    """
    return "".join(_OPT_PREFIX + (name, "=", param))
