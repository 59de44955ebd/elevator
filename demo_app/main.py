from elevator import *

import os
import sys

from ctypes import *
from ctypes.wintypes import *

IS_64_BIT = sys.maxsize > 2**32

########################################
# Used Winapi typedefs
########################################
LONG_PTR = c_longlong if IS_64_BIT else c_long
WNDPROC = WINFUNCTYPE(LONG_PTR, HWND, UINT, WPARAM, LPARAM)

########################################
# Used Winapi constants
########################################
BN_CLICKED = 0
BS_PUSHBUTTON = 0
COLOR_3DFACE = 15
CS_HREDRAW = 2
CS_VREDRAW = 1
CW_USEDEFAULT = -2147483648
DEFAULT_GUI_FONT = 17
ES_MULTILINE = 4
GWL_WNDPROC = -4
IDC_ARROW = 32512
IMAGE_ICON = 1
LR_LOADFROMFILE = 16
SW_SHOWNORMAL = 1
WC_BUTTON = 'Button'
WC_EDIT = 'EDIT'
WM_CLOSE = 16
WM_COMMAND = 273
WM_QUIT = 18
WM_SETFONT = 48
WS_BORDER = 8388608
WS_CAPTION = 12582912
WS_CHILD = 1073741824
WS_OVERLAPPED = 0
WS_SYSMENU = 524288
WS_VISIBLE = 268435456

########################################
# Used Winapi macros
########################################

def MAKEINTRESOURCEW(x):
    return LPCWSTR(x)

def MAKELONG(wLow, wHigh):
    return LONG(wLow | wHigh << 16).value

def MAKELPARAM(l, h):
    return LPARAM(MAKELONG(l, h)).value

def HIWORD(l):
    return WORD((l >> 16) & 0xFFFF).value

def LOWORD(l):
    return WORD(l & 0xFFFF).value

########################################
# Used Winapi structs
########################################

class WNDCLASSEXW(Structure):
    def __init__(self, *args, **kwargs):
        super(WNDCLASSEXW, self).__init__(*args, **kwargs)
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
# Used Winapi functions
########################################

gdi32 = windll.gdi32
gdi32.GetStockObject.restype = HANDLE

kernel32 = windll.kernel32
kernel32.GetModuleHandleW.argtypes = (LPCWSTR,)
kernel32.GetModuleHandleW.restype = HMODULE

user32 = windll.user32
user32.RegisterClassExW.argtypes = (LPVOID,)  # POINTER(WNDCLASSEXW)
user32.CreateWindowExW.argtypes = (DWORD, LPCWSTR, LPCWSTR, DWORD, INT, INT, INT, INT, HWND, HMENU, HINSTANCE, LPVOID)
user32.DefWindowProcW.argtypes = (HWND, c_uint, WPARAM, LPARAM)
user32.DestroyWindow.argtypes = (HWND,)
user32.DispatchMessageW.argtypes = (POINTER(MSG),)
user32.GetMessageW.argtypes = (POINTER(MSG),HWND,UINT,UINT)
user32.LoadIconW.argtypes = (HINSTANCE, LPCWSTR)
user32.LoadIconW.restype = HICON
user32.LoadImageW.argtypes = (HINSTANCE, LPCWSTR, UINT, INT, INT, UINT)
user32.LoadImageW.restype = HANDLE
user32.PostMessageW.argtypes = (HWND, UINT, LPVOID, LPVOID)
user32.PostMessageW.restype = LONG_PTR
user32.SendMessageW.argtypes = (HWND, UINT, LPVOID, LPVOID)  # LPVOID to allow to send pointers
user32.SendMessageW.restype = LONG_PTR
user32.SetWindowLongPtrW.argtypes = (HWND, LONG_PTR, WNDPROC)
user32.SetWindowLongPtrW.restype = WNDPROC
user32.TranslateMessage.argtypes = (POINTER(MSG),)


########################################
# Base Class
########################################
class Window(object):

    def __init__(
        self,
        window_class,
        style = WS_CHILD | WS_VISIBLE,
        ex_style = 0,
        left = 0, top = 0, width = 0, height = 0,
        window_title = None,
        h_font = None,
        h_menu = 0,
        parent_window = None,
        h_instance = 0
    ):
        self.hwnd = user32.CreateWindowExW(
            ex_style,
            window_class,
            window_title,
            style,
            left, top, width, height,
            parent_window.hwnd if parent_window else 0,
            h_menu,
            h_instance,
            0  # lpParam
        )
        if h_font:
            user32.SendMessageW(self.hwnd, WM_SETFONT, h_font, MAKELPARAM(1, 0))


########################################
#
########################################
class App(Window):

    def __init__(self):

        # Create main window
        if IS_FROZEN:
            h_icon = user32.LoadIconW(kernel32.GetModuleHandleW(None), MAKEINTRESOURCEW(1))
        else:
            h_icon = user32.LoadImageW(0, os.path.join(os.path.dirname(__file__), 'app.ico'), IMAGE_ICON, 16, 16, LR_LOADFROMFILE)

        def _window_proc_callback(hwnd, msg, wparam, lparam):
            if msg == WM_CLOSE:
                user32.PostMessageW(self.hwnd, WM_QUIT, 0, 0)
            elif msg == WM_COMMAND:
                control_id = LOWORD(wparam)
                command = HIWORD(wparam)
                if command == BN_CLICKED:

                    if lparam == button_toggle.hwnd:
                        if IS_ELEVATED:
                            exec_unelevated(sys.executable, params=None if IS_FROZEN else os.path.realpath(__file__), show=1)
                        else:
                            exec_elevated(sys.executable, params=None if IS_FROZEN else os.path.realpath(__file__), show=1)
                        self.quit()

                    elif lparam == button_elevated_command.hwnd:
                        stdout, stderr, exit_code = run_elevated_command(r'cmd /c dir %windir%\system32\config\systemprofile')
                        if exit_code == 0:
                            user32.SetWindowTextW(edit.hwnd, stdout.decode('oem'))
                        else:
                            user32.SetWindowTextW(edit.hwnd, f'ERROR: {exit_code} - {stderr.decode("oem")}')

                    elif lparam == button_unelevated_command.hwnd:
                        stdout, stderr, exit_code = run_unelevated_command(r"cmd /c dir %windir%\system32\config\systemprofile")
                        if exit_code == 0:
                            user32.SetWindowTextW(edit.hwnd, stdout.decode('oem'))
                        else:
                            user32.SetWindowTextW(edit.hwnd, f'ERROR: {exit_code} - {stderr.decode("oem")}')

            return user32.DefWindowProcW(hwnd, msg, wparam, lparam)

        self.windowproc = WNDPROC(_window_proc_callback)

        new_class = WNDCLASSEXW()
        new_class.lpfnWndProc = self.windowproc
        new_class.style = CS_VREDRAW | CS_HREDRAW
        new_class.lpszClassName = 'MyDemoClass'
        new_class.hBrush = COLOR_3DFACE + 1
        new_class.hCursor = user32.LoadCursorW(0, IDC_ARROW)
        new_class.hIcon = h_icon
        user32.RegisterClassExW(byref(new_class))

        super().__init__(
            new_class.lpszClassName,
            style = WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU,
            left = CW_USEDEFAULT, top = CW_USEDEFAULT, width = 476, height = 320,
            window_title = f"Application is {'ELEVATED' if IS_ELEVATED else 'UNELEVATED'}",
        )

        # Create buttons
        button_toggle = Window(
            WC_BUTTON,
            parent_window = self,
            style = WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON,
            left = 10, top = 10, width = 140, height = 24,
            window_title = 'Unelevate application' if IS_ELEVATED else 'Elevate application',
            h_font = gdi32.GetStockObject(DEFAULT_GUI_FONT)
        )

        button_elevated_command = Window(
            WC_BUTTON,
            parent_window = self,
            style = WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON,
            left = 155, top = 10, width = 140, height = 24,
            window_title = 'Run elevated command',
            h_font = gdi32.GetStockObject(DEFAULT_GUI_FONT)
        )

        button_unelevated_command = Window(
            WC_BUTTON,
            parent_window = self,
            style = WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON,
            left = 300, top = 10, width = 150, height = 24,
            window_title = 'Run unelevated command',
            h_font = gdi32.GetStockObject(DEFAULT_GUI_FONT)
        )

        # Create edit control
        edit = Window(
            WC_EDIT,
            parent_window = self,
            style = WS_CHILD | WS_VISIBLE | WS_BORDER | ES_MULTILINE,
            left = 10, top = 44, width = 440, height = 226,
            h_font = gdi32.GetStockObject(DEFAULT_GUI_FONT)
        )

        user32.ShowWindow(self.hwnd, SW_SHOWNORMAL)

    def run(self):
        msg = MSG()
        while user32.GetMessageW(byref(msg), 0, 0, 0) > 0:
            user32.TranslateMessage(byref(msg))
            user32.DispatchMessageW(byref(msg))
        user32.DestroyWindow(self.hwnd)
        return 0

    def quit(self, *args):
        user32.PostMessageW(self.hwnd, WM_QUIT, 0, 0)


if __name__ == '__main__':
    sys.exit(App().run())
