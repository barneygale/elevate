import ctypes
import elevate.elevate_util as elevate_util
from ctypes import POINTER, c_ulong, c_char_p, c_int, c_void_p
from ctypes.wintypes import HANDLE, BOOL, DWORD, HWND, HINSTANCE, HKEY
from ctypes import windll
import subprocess
import sys
from os.path import abspath
# Constant defintions


SEE_MASK_NOCLOSEPROCESS = 0x00000040
SEE_MASK_NO_CONSOLE = 0x00008000


# Type definitions

PHANDLE = ctypes.POINTER(HANDLE)
PDWORD = ctypes.POINTER(DWORD)


class ShellExecuteInfo(ctypes.Structure):
    _fields_ = [
        ('cbSize',       DWORD),
        ('fMask',        c_ulong),
        ('hwnd',         HWND),
        ('lpVerb',       c_char_p),
        ('lpFile',       c_char_p),
        ('lpParameters', c_char_p),
        ('lpDirectory',  c_char_p),
        ('nShow',        c_int),
        ('hInstApp',     HINSTANCE),
        ('lpIDList',     c_void_p),
        ('lpClass',      c_char_p),
        ('hKeyClass',    HKEY),
        ('dwHotKey',     DWORD),
        ('hIcon',        HANDLE),
        ('hProcess',     HANDLE)]

    def __init__(self, **kw):
        super(ShellExecuteInfo, self).__init__()
        self.cbSize = ctypes.sizeof(self)
        for field_name, field_value in kw.items():
            setattr(self, field_name, field_value)


PShellExecuteInfo = POINTER(ShellExecuteInfo)


# Function definitions

ShellExecuteEx = windll.shell32.ShellExecuteExA
ShellExecuteEx.argtypes = (PShellExecuteInfo, )
ShellExecuteEx.restype = BOOL

WaitForSingleObject = windll.kernel32.WaitForSingleObject
WaitForSingleObject.argtypes = (HANDLE, DWORD)
WaitForSingleObject.restype = DWORD

CloseHandle = windll.kernel32.CloseHandle
CloseHandle.argtypes = (HANDLE, )
CloseHandle.restype = BOOL


# At last, the actual implementation!

def elevate(show_console=True, graphical=True, restore_cwd=True):
    # sys.argv is changed
    # check both values just in case _process_elevate_opts wasn't
    #   already called on import
    elevate_opts = elevate_util._process_elevate_opts() \
        or elevate_util._ELEVATE_GOT_ARGS

    if (windll.shell32.IsUserAnAdmin()
            # prevent infinite recursion in all cases
            or elevate_util._get_opt(elevate_opts, "invocation")):
        return

    params = ShellExecuteInfo(
        fMask=SEE_MASK_NOCLOSEPROCESS | SEE_MASK_NO_CONSOLE,
        hwnd=None,
        lpVerb=b'runas',
        lpFile=sys.executable.encode('cp1252'),
        lpParameters=subprocess.list2cmdline(
            [
                abspath(sys.argv[0]),
                elevate_util._make_opt("invocation", "True")
            ] + sys.argv[1:]
        ).encode('cp1252'),
        nShow=int(show_console))

    if not ShellExecuteEx(ctypes.byref(params)):
        raise ctypes.WinError()

    handle = params.hProcess
    ret = DWORD()
    WaitForSingleObject(handle, -1)

    if windll.kernel32.GetExitCodeProcess(handle, ctypes.byref(ret)) == 0:
        raise ctypes.WinError()

    CloseHandle(handle)
    sys.exit(ret.value)
