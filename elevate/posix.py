import errno
import elevate.elevate_util as elevate_util
import os
import sys
try:
    from shlex import quote
except ImportError:
    from pipes import quote


def quote_shell(args):
    return " ".join(quote(arg) for arg in args)


def quote_applescript(string):
    charmap = {
        "\n": "\\n",
        "\r": "\\r",
        "\t": "\\t",
        "\"": "\\\"",
        "\\": "\\\\",
    }
    return '"%s"' % "".join(charmap.get(char, char) for char in string)


def elevate(show_console=True, graphical=True, restore_cwd=True):
    # sys.argv has been changed here
    # check both values just in case _process_elevate_opts wasn't
    #   already called on import
    elevate_opts = elevate_util._process_elevate_opts() \
        or elevate_util._ELEVATE_GOT_ARGS

    if os.getuid() == 0:
        newdir = elevate_util._get_opt(elevate_opts, "cwd")
        if newdir and restore_cwd:
            try:                      os.chdir(newdir)
            except FileNotFoundError: pass
            except Exception as e:    raise
        return

    # prevent infinite recursion in all cases
    if elevate_util._get_opt(elevate_opts, "invocation"):
        return

    args = [
        sys.executable,
        os.path.abspath(sys.argv[0]),
        elevate_util._make_opt("invocation", "True")
    ] + sys.argv[1:]

    # some argument parsers can't understand empty command-line options like ""
    #   so an explicit conditional append is needed
    if restore_cwd:
        args.append( elevate_util._make_opt("cwd", os.getcwd()) )

    commands = []

    if graphical:
        if sys.platform.startswith("darwin"):
            commands.append([
                "osascript",
                "-e",
                "do shell script %s "
                "with administrator privileges "
                "without altering line endings"
                % quote_applescript(quote_shell(args))])

        if sys.platform.startswith("linux") and os.environ.get("DISPLAY"):
            commands.append(["pkexec"] + args)
            commands.append(["gksudo"] + args)
            commands.append(["kdesudo"] + args)

    commands.append(["sudo"] + args)

    for args in commands:
        try:
            os.execlp(args[0], *args)
        except OSError as e:
            if e.errno != errno.ENOENT or args[0] == "sudo":
                raise
