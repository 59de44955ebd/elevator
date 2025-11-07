__all__ = ['IS_ELEVATED', 'exec_elevated', 'exec_unelevated', 'run_elevated_command', 'run_unelevated_command']

from ctypes import *
from ctypes.wintypes import *
import sys

IS_64_BIT = sys.maxsize > 2**32
IS_FROZEN = getattr(sys, 'frozen', False)

########################################
# Winapi TypeDefs
########################################

LONG_PTR = c_longlong if IS_64_BIT else c_long
ULONG_PTR = c_uint64 if IS_64_BIT else c_ulong
WNDPROC = WINFUNCTYPE(LONG_PTR, HWND, UINT, WPARAM, LPARAM)

########################################
# Winapi Constants
########################################

DUPLICATE_SAME_ACCESS = 2
FALSE = 0
INFINITE = 0xFFFFFFFF
INVALID_HANDLE_VALUE = -1
PROCESS_QUERY_INFORMATION = 0x0400
SECURITY_IMPERSONATION = 2
SEE_MASK_NOCLOSEPROCESS = 0x00000040
SEE_MASK_NOCLOSEPROCESS = 0x00000040
STARTF_USESHOWWINDOW = 1
STARTF_USESTDHANDLES = 256
TH32CS_SNAPPROCESS = 0x00000002
TOKEN_ALL_ACCESS = 0xF01FF
TOKEN_DUPLICATE = 0x0002
TOKEN_PRIMARY = 1
TRUE = 1
WM_COPYDATA = 74
WM_QUIT = 18
WS_OVERLAPPEDWINDOW = 13565952

########################################
# Winapi Structs
########################################

class COPYDATASTRUCT(Structure):
    _fields_ = [
        ('dwData', LPARAM),
        ('cbData', DWORD),
        ('lpData', LPVOID)
    ]

class PROCESSENTRY32W(Structure):
    def __init__(self, *args, **kwargs):
        super(PROCESSENTRY32W, self).__init__(*args, **kwargs)
        self.dwSize = sizeof(self)
    _fields_ = [
        ('dwSize',              DWORD),
        ('cntUsage',            DWORD),
        ('th32ProcessID',       DWORD),
        ('th32DefaultHeapID',   ULONG_PTR),
        ('th32ModuleID',        DWORD),
        ('cntThreads',          DWORD),
        ('th32ParentProcessID', DWORD),
        ('pcPriClassBase',      LONG),
        ('dwFlags',             DWORD),
        ('szExeFile',           WCHAR * MAX_PATH),
    ]

class PROCESS_INFORMATION(Structure):
    _fields_ = [
        ('hProcess',            HANDLE),
        ('hThread',             HANDLE),
        ('dwProcessId',         DWORD),
        ('dwThreadId',          DWORD),
    ]

class SECURITY_ATTRIBUTES(Structure):
    def __init__(self, *args, **kwargs):
        super(SECURITY_ATTRIBUTES, self).__init__(*args, **kwargs)
        self.nLength = sizeof(self)
    _fields_ = [
        ('nLength',                 DWORD),
        ('lpSecurityDescriptor',    LPVOID),
        ('bInheritHandle',          BOOL),
    ]

class SHELLEXECUTEINFOW(Structure):
    def __init__(self, *args, **kwargs):
        super(SHELLEXECUTEINFOW, self).__init__(*args, **kwargs)
        self.cbSize = sizeof(self)
    _fields_ = [
        ('cbSize',          DWORD),
        ('fMask',           ULONG),
        ('hwnd',            HWND),
        ('lpVerb',          LPCWSTR),
        ('lpFile',          LPCWSTR),
        ('lpParameters',    LPCWSTR),
        ('lpDirectory',     LPCWSTR),
        ('nShow',           INT),
        ('hInstApp',        HINSTANCE),
        ('lpIDList',        LPVOID),
        ('lpClass',         LPCWSTR),
        ('hkeyClass',       HKEY),
        ('dwHotKey',        DWORD),
        ('hIcon',           HANDLE),
        ('hProcess',        HANDLE)
    ]

class STARTUPINFOW(Structure):
    def __init__(self, *args, **kwargs):
        super(STARTUPINFOW, self).__init__(*args, **kwargs)
        self.cb = sizeof(self)
    _fields_ = [
        ('cb',                    DWORD ),
        ('lpReserved',            LPWSTR),
        ('lpDesktop',             LPWSTR),
        ('lpTitle',               LPWSTR),
        ('dwX',                   DWORD),
        ('dwY',                   DWORD),
        ('dwXSize',               DWORD),
        ('dwYSize',               DWORD),
        ('dwXCountChars',         DWORD),
        ('dwYCountChars',         DWORD),
        ('dwFillAttribute',       DWORD),
        ('dwFlags',               DWORD),
        ('wShowWindow',           WORD),
        ('cbReserved2',           WORD),
        ('lpReserved2',           LPBYTE),
        ('hStdInput',             HANDLE),
        ('hStdOutput',            HANDLE),
        ('hStdError',             HANDLE),
    ]

class WNDCLASSEX(Structure):
    def __init__(self, *args, **kwargs):
        super(WNDCLASSEX, self).__init__(*args, **kwargs)
        self.cbSize = sizeof(self)
    _fields_ = [
        ('cbSize', c_uint),
        ('style', c_uint),
        ('lpfnWndProc', WNDPROC),
        ('cbClsExtra', c_int),
        ('cbWndExtra', c_int),
        ('hInstance', HANDLE),
        ('hIcon', HANDLE),
        ('hCursor', HANDLE),
        ('hBrush', HANDLE),
        ('lpszMenuName', LPCWSTR),
        ('lpszClassName', LPCWSTR),
        ('hIconSm', HANDLE)
    ]

########################################
# Winapi Functions
########################################

advapi32 = windll.Advapi32
advapi32.CreateProcessWithTokenW.argtypes = (HANDLE, DWORD, LPCWSTR, LPWSTR, DWORD, LPVOID, LPCWSTR, POINTER(STARTUPINFOW), POINTER(PROCESS_INFORMATION))
advapi32.DuplicateTokenEx.argtypes = (HANDLE, DWORD, LPVOID, INT, INT, POINTER(HANDLE))
advapi32.OpenProcessToken.argtypes = (HANDLE, DWORD, POINTER(HANDLE))

kernel32 = windll.Kernel32
kernel32.CloseHandle.argtypes = (HANDLE,)
kernel32.CreatePipe.argtypes = (POINTER(HANDLE), POINTER(HANDLE), POINTER(SECURITY_ATTRIBUTES), DWORD)
kernel32.CreateProcessW.argtypes = (LPCWSTR, LPWSTR, POINTER(SECURITY_ATTRIBUTES), POINTER(SECURITY_ATTRIBUTES), BOOL, DWORD, LPVOID, LPCWSTR, POINTER(STARTUPINFOW), POINTER(PROCESS_INFORMATION))
kernel32.CreateToolhelp32Snapshot.argtypes = (DWORD, DWORD)
kernel32.CreateToolhelp32Snapshot.restype = HANDLE
kernel32.DuplicateHandle.argtypes = (HANDLE, HANDLE, HANDLE, POINTER(HANDLE), DWORD, BOOL, DWORD)
kernel32.GetCurrentProcess.restype = HANDLE
kernel32.GetExitCodeProcess.argtypes = (HANDLE, LPDWORD)
kernel32.GetExitCodeProcess.argtypes = (HANDLE, LPDWORD)
kernel32.GetProcessId.argtypes = (HANDLE,)
kernel32.OpenProcess.argtypes = (DWORD, BOOL, DWORD)
kernel32.OpenProcess.restype = HANDLE
kernel32.PeekNamedPipe.argtypes = (HANDLE, LPVOID, DWORD, POINTER(DWORD), POINTER(DWORD), POINTER(DWORD))
kernel32.Process32FirstW.argtypes = (HANDLE, POINTER(PROCESSENTRY32W))
kernel32.Process32NextW.argtypes = (HANDLE, POINTER(PROCESSENTRY32W))
kernel32.ReadFile. argtypes = (HANDLE, LPVOID, DWORD, POINTER(DWORD), LPVOID)  #POINTER(OVERLAPPED))
kernel32.WaitForSingleObject.argtypes = (HANDLE, DWORD)

shell32 = windll.shell32
shell32.ShellExecuteExW.argtypes = (POINTER(SHELLEXECUTEINFOW),)

user32 = windll.user32
user32.CreateWindowExW.argtypes = (DWORD, LPCWSTR, LPCWSTR, DWORD, INT, INT, INT, INT, HWND, HMENU, HINSTANCE, LPVOID)
user32.DefWindowProcW.argtypes = (HWND, c_uint, WPARAM, LPARAM)
user32.DestroyWindow.argtypes = (HWND,)
user32.DispatchMessageW.argtypes = (POINTER(MSG),)
user32.GetMessageW.argtypes = (POINTER(MSG),HWND,UINT,UINT)
user32.PostMessageW.argtypes = (HWND, UINT, LPVOID, LPVOID)
user32.PostMessageW.restype = LONG_PTR
user32.SendMessageW.argtypes = (HWND, UINT, LPVOID, LPVOID)
user32.SendMessageW.restype = LONG_PTR
user32.TranslateMessage.argtypes = (POINTER(MSG),)

IS_ELEVATED = shell32.IsUserAnAdmin()

########################################
#
########################################
def _get_pid(process_name: str) -> int:
    h_process_snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if h_process_snapshot == INVALID_HANDLE_VALUE:
        return 0
    pe = PROCESSENTRY32W()
    if not kernel32.Process32FirstW(h_process_snapshot, byref(pe)):
        kernel32.CloseHandle(h_process_snapshot)
        return 0
    while True:
        if process_name == pe.szExeFile:
            kernel32.CloseHandle(h_process_snapshot)
            return pe.th32ProcessID
        if not kernel32.Process32NextW(h_process_snapshot, byref(pe)):
            break
    kernel32.CloseHandle(h_process_snapshot)
    return 0

########################################
#
########################################
def exec_elevated(exe: str, params: str = None, cwd: str = None, show: int = 0, wait: bool = False) -> bool | int:
    exec_info = SHELLEXECUTEINFOW()
    exec_info.nShow = show
    exec_info.fMask = SEE_MASK_NOCLOSEPROCESS
    exec_info.lpVerb = 'runas'
    exec_info.lpFile = exe
    exec_info.lpParameters = params
    if cwd:
        exec_info.lpDirectory = cwd
    if not shell32.ShellExecuteExW(byref(exec_info)):
        return False
    if wait:
        kernel32.WaitForSingleObject(exec_info.hProcess, INFINITE)
        exit_code = DWORD()
        ok = kernel32.GetExitCodeProcess(exec_info.hProcess, byref(exit_code))
        return exit_code.value
    else:
        return kernel32.GetProcessId(exec_info.hProcess)

########################################
#
########################################
def exec_unelevated(exe: str, params: str = None, cwd: str = None, show: int = 0, wait: bool = False) -> bool | int:

    if not IS_ELEVATED:
        exec_info = SHELLEXECUTEINFOW()
        exec_info.nShow = show
        exec_info.fMask = SEE_MASK_NOCLOSEPROCESS
        exec_info.lpFile = exe
        exec_info.lpParameters = params
        exec_info.lpDirectory = cwd
        if not shell32.ShellExecuteExW(byref(exec_info)):
            return False
        if wait:
            kernel32.WaitForSingleObject(exec_info.hProcess, INFINITE)
            exit_code = DWORD()
            kernel32.GetExitCodeProcess(exec_info.hProcess, byref(exit_code))
            return exit_code.value
        else:
            return kernel32.GetProcessId(exec_info.hProcess)

    pid_explorer = _get_pid("explorer.exe")
    if not pid_explorer:
        raise Exception(f'Getting Explorer PID failed with error {kernel32.GetLastError()}')

    h_process = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, 0, pid_explorer)
    if not h_process:
        raise Exception(f'OpenProcess failed with error {kernel32.GetLastError()}')

    token_handle = HANDLE()
    ok = advapi32.OpenProcessToken(h_process, TOKEN_DUPLICATE, byref(token_handle))
    if not ok:
        kernel32.CloseHandle(h_process)
        raise Exception(f'OpenProcessToken failed with error {kernel32.GetLastError()}')

    # Duplicate the token handle
    new_token_handle = HANDLE()
    ok = advapi32.DuplicateTokenEx(token_handle, TOKEN_ALL_ACCESS, None, SECURITY_IMPERSONATION, TOKEN_PRIMARY, byref(new_token_handle))

    kernel32.CloseHandle(token_handle)
    kernel32.CloseHandle(h_process)

    if not ok:
        raise Exception(f'DuplicateTokenEx failed with error {kernel32.GetLastError()}')

    # Special case: CreateProcessWithTokenW() fails if app to run is explorer, so we use a (hidden) CMD as "proxy"
    if exe.lower() == 'explorer.exe':
        exe = 'cmd.exe'
        params = f'/c start explorer {params}' if params else '/c start explorer'
        show = 0

    startup_info = STARTUPINFOW()
    startup_info.dwFlags = STARTF_USESHOWWINDOW
    startup_info.wShowWindow = show

    proc_info = PROCESS_INFORMATION()

    ok = advapi32.CreateProcessWithTokenW(new_token_handle, 0, exe, params, 0, None, cwd, byref(startup_info), byref(proc_info))
    if not ok:
        raise Exception(f'CreateProcessWithTokenW failed with error {kernel32.GetLastError()}')

    if wait:
        kernel32.WaitForSingleObject(proc_info.hProcess, INFINITE)
        exit_code = DWORD()
        kernel32.GetExitCodeProcess(proc_info.hProcess, byref(exit_code))
        res = exit_code.value
    else:
        res = proc_info.dwProcessId

    kernel32.CloseHandle(proc_info.hThread)
    kernel32.CloseHandle(proc_info.hProcess)

    return res

def _run(command_line: str, cwd: str = '', unelevate: bool = False) -> tuple[bytes, bytes, int]:

    h_child_stdout_read = HANDLE()
    h_child_stdout_write = HANDLE()
    h_child_stdout_read_dup = HANDLE()

    h_child_stderr_read = HANDLE()
    h_child_stderr_write = HANDLE()
    h_child_stderr_read_dup = HANDLE()

    sec_attr = SECURITY_ATTRIBUTES()
    sec_attr.bInheritHandle = TRUE

    # Create a pipe for the child process's STDOUT.
    if not kernel32.CreatePipe(byref(h_child_stdout_read), byref(h_child_stdout_write), byref(sec_attr), 0):
        raise Exception(f'CreatePipe failed with error {kernel32.GetLastError()}')

    # Create a pipe for the child process's STDERR.
    if not kernel32.CreatePipe(byref(h_child_stderr_read), byref(h_child_stderr_write), byref(sec_attr), 0):
        raise Exception(f'CreatePipe failed with error {kernel32.GetLastError()}')

    h_proc = kernel32.GetCurrentProcess()

    # Create noninheritable read handle and close the inheritable read handle.
    ok = kernel32.DuplicateHandle(
        h_proc,
        h_child_stdout_read,
        h_proc,
        byref(h_child_stdout_read_dup),
        0,
        FALSE,
        DUPLICATE_SAME_ACCESS
    )

    kernel32.CloseHandle(h_child_stdout_read)

    if not ok:
        kernel32.CloseHandle(h_child_stderr_read)
        raise Exception(f'DuplicateHandle failed for STDOUT with error {kernel32.GetLastError()}')

    # Create noninheritable read handle and close the inheritable read handle.
    ok = kernel32.DuplicateHandle(
        h_proc,
        h_child_stderr_read,
        h_proc,
        byref(h_child_stderr_read_dup),
        0,
        FALSE,
        DUPLICATE_SAME_ACCESS
    )

    kernel32.CloseHandle(h_child_stderr_read)

    if not ok:
        raise Exception(f'DuplicateHandle failed for STDERR with error {kernel32.GetLastError()}')

    startup_info = STARTUPINFOW()
    startup_info.hStdError = h_child_stderr_write
    startup_info.hStdOutput = h_child_stdout_write
    startup_info.dwFlags = STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW

    proc_info = PROCESS_INFORMATION()

    if IS_ELEVATED and unelevate:
        pid_explorer = _get_pid("explorer.exe")
        if not pid_explorer:
            raise Exception(f'Getting Explorer PID failed with error {kernel32.GetLastError()}')

        h_process = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, 0, pid_explorer)
        if not h_process:
            raise Exception(f'OpenProcess failed with error {kernel32.GetLastError()}')

        token_handle = HANDLE()
        ok = advapi32.OpenProcessToken(h_process, TOKEN_DUPLICATE, byref(token_handle))
        if not ok:
            kernel32.CloseHandle(hProcess)
            raise Exception(f'OpenProcessToken failed with error {kernel32.GetLastError()}')

        # Duplicate the token handle
        new_token_handle = HANDLE()
        ok = advapi32.DuplicateTokenEx(token_handle, TOKEN_ALL_ACCESS, None, SECURITY_IMPERSONATION, TOKEN_PRIMARY, byref(new_token_handle))

        kernel32.CloseHandle(token_handle)
        kernel32.CloseHandle(h_process)

        if not ok:
            raise Exception(f'DuplicateTokenEx failed with error {kernel32.GetLastError()}')

        ok = advapi32.CreateProcessWithTokenW(
            new_token_handle,
            0,                  # dwLogonFlags
            None,
            command_line,
            0,                  # dwCreationFlags
            None,               # use parent's environment
            cwd if cwd else None,
            byref(startup_info),
            byref(proc_info)
        )

        if not ok:
            raise Exception(f'CreateProcessWithTokenW failed with error {kernel32.GetLastError()}')

    else:

        ok = kernel32.CreateProcessW(
            None,
            command_line,
            None,               # process security attributes
            None,               # primary thread security attributes
            TRUE,               # handles are inherited
            0,                  # dwCreationFlags
            None,               # use parent's environment
            cwd if cwd else None,
            byref(startup_info),
            byref(proc_info)
        )

        if not ok:
            raise Exception(f'CreateProcess failed with error {kernel32.GetLastError()}')

    kernel32.CloseHandle(proc_info.hThread)

    # Close the write end of the pipe before reading from the read end of the pipe.
    if not kernel32.CloseHandle(h_child_stdout_write):
        kernel32.CloseHandle(proc_info.hProcess)
        raise Exception(f'CloseHandle failed for STDOUT with error {kernel32.GetLastError()}')
    if not kernel32.CloseHandle(h_child_stderr_write):
        kernel32.CloseHandle(proc_info.hProcess)
        raise Exception(f'CloseHandle failed for STDERR with error {kernel32.GetLastError()}')

    bytes_available = DWORD()
    res_stdout = bytearray()
    res_stderr = bytearray()

    while True:

        # stdout
        ok = kernel32.PeekNamedPipe(h_child_stdout_read_dup, None, 0, None, byref(bytes_available), None)
        if not ok:
            break
        if bytes_available.value:
            buf = create_string_buffer(bytes_available.value)
            kernel32.ReadFile(h_child_stdout_read_dup, buf, bytes_available, None, None)
            res_stdout += buf.value

        # stderr
        ok = kernel32.PeekNamedPipe(h_child_stderr_read_dup, None, 0, None, byref(bytes_available), None)
        if not ok:
            break
        if bytes_available.value:
            buf = create_string_buffer(bytes_available.value)
            kernel32.ReadFile(h_child_stderr_read_dup, buf, bytes_available, None, None)
            res_stderr += buf.value

    exit_code = DWORD()
    kernel32.GetExitCodeProcess(proc_info.hProcess, byref(exit_code))
    kernel32.CloseHandle(proc_info.hProcess)

    return bytes(res_stdout), bytes(res_stderr), exit_code.value


class _Receiver():

    def __init__(self):
        self.data_out, self.data_err, self.exit_code = b'', b'', 1

        def _window_proc_callback(hwnd, msg, wparam, lparam):
            if msg == WM_COPYDATA:
                cds = cast(lparam, POINTER(COPYDATASTRUCT)).contents
                data = cast(cds.lpData, LPCSTR).value
                self.data_out = data[:cds.dwData]
                self.data_err = data[cds.dwData:]
                self.exit_code = wparam
                user32.PostMessageW(hwnd, WM_QUIT, 0, 0)
            return user32.DefWindowProcW(hwnd, msg, wparam, lparam)

        self.windowproc = WNDPROC(_window_proc_callback)
        newclass = WNDCLASSEX()
        newclass.lpfnWndProc = self.windowproc
        newclass.lpszClassName = 'ReceiverClass'
        user32.RegisterClassExW(byref(newclass))
        self.hwnd = user32.CreateWindowExW(
            0,
            newclass.lpszClassName,
            'Receiver',
            WS_OVERLAPPEDWINDOW,
            0, 0, 0, 0,
            None, None, None, None
        )

    def run(self, command_line: str, cwd: str = '') -> tuple[bytes, bytes, int]:
        if cwd.endswith('\\'):
            cwd += '\\'
        command_line = f'-m elevator "{[self.hwnd, command_line, cwd]}"'
        if exec_elevated(sys.executable, command_line) != False:
            msg = MSG()
            while user32.GetMessageW(byref(msg), 0, 0, 0) > 0:
                user32.TranslateMessage(byref(msg))
                user32.DispatchMessageW(byref(msg))
        user32.DestroyWindow(self.hwnd)
        return self.data_out, self.data_err, self.exit_code


########################################
#
########################################
def run_elevated_command(command_line: str, cwd: str = '') -> tuple[bytes, bytes, int]:
    return _Receiver().run(command_line, cwd)

########################################
#
########################################
def run_unelevated_command(command_line: str, cwd: str = '') -> tuple[bytes, bytes, int]:
    return _run(command_line, cwd, unelevate=True)

# For internal use only
if __name__ == '__main__' or (IS_FROZEN and len(sys.argv) > 3 and sys.argv[1] == '-m'  and sys.argv[2] == 'elevator'):

    hwnd, command_line, cwd = eval(sys.argv[3 if IS_FROZEN else 1])
    try:
        data_out, data_err, exit_code = _run(command_line, cwd)
    except Exception as e:
        data_out, data_err, exit_code = b'', str(e).encode(), 2
    out_len = len(data_out)
    data = data_out + data_err
    cds = COPYDATASTRUCT(out_len, len(data) + 1, cast(LPCSTR(data), LPVOID))
    user32.SendMessageW(hwnd, WM_COPYDATA, exit_code, byref(cds))

    sys.exit(0)
