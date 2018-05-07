import ctypes
from ctypes import POINTER, c_ulong, c_char_p, c_int, c_void_p
from ctypes.wintypes import HANDLE, BOOL, DWORD, HWND, HINSTANCE, HKEY
from ctypes.windll import shell32, kernel32
import subprocess
import sys

try:
    unicode
except NameError:
    def unicode(s):
        return s

# Constant defintions

SW_HIDE = 0
SW_SHOW = 5
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

ShellExecuteEx = shell32.ShellExecuteExA
ShellExecuteEx.argtypes = (PShellExecuteInfo, )
ShellExecuteEx.restype = BOOL

WaitForSingleObject = kernel32.WaitForSingleObject
WaitForSingleObject.argtypes = (HANDLE, DWORD)
WaitForSingleObject.restype = DWORD

CloseHandle = kernel32.CloseHandle
CloseHandle.argtypes = (HANDLE, )
CloseHandle.restype = BOOL


# At last, the actual implementation!

def elevate():
    if shell32.IsUserAnAdmin():
        return
    params = ShellExecuteInfo(
        fMask=SEE_MASK_NOCLOSEPROCESS | SEE_MASK_NO_CONSOLE,
        hwnd=None,
        lpVerb=unicode('runas'),
        lpFile=unicode(sys.executable),
        lpParameters=unicode(subprocess.list2cmdline(sys.argv)),
        nShow=SW_SHOW)

    if not ShellExecuteEx(ctypes.byref(params)):
        raise ctypes.WinError()

    handle = params.hProcess
    ret = DWORD()
    WaitForSingleObject(handle, -1)
    if kernel32.GetExitCodeProcess(handle, ctypes.byref(ret)) == 0:
        raise ctypes.WinError()

    CloseHandle(handle)
    sys.exit(ret)
