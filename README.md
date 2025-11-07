# elevator

A Python 3 module for Windows 10/11 for dealing with elevation/UAC.

## Functions

The module implements the following 4 public functions:

### 1.) exec_elevated()

```
exec_elevated(exe: str, params: str = None, cwd: str = None, show: int = 0, wait: bool = False) -> bool | int
```
Allows to run an elevated exe from an unelevated Python process/app via ShellExecute. The user will get an UAC prompt and has to confirm it. 

If the process could not be started, either because the specified exe doesn't exist or the user did not confirm the UAC prompt, the function returns `False`.

Otherwise the process id (`int`) is returned, unless `wait=True` is specified, in this case instead the exit code (`int`) of the process is returned.

The `show` parameter (`int`) specifies if/how the window of the process is displayed, it defaults to 0 (SW_HIDE), i.e. the window is hidden. To show it specify 1 (SW_SHOWNORMAL). See [here](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow) for other possible values.

Usage example:
```python
from elevator import exec_elevated

# pid = exec_elevated("sc.exe", params="stop Spooler")

exit_code = exec_elevated("sc.exe", params="stop Spooler", wait=True)

print(exit_code)  # 0 if spooler service was stopped successfully
```

### 2.) exec_unelevated()

```
exec_unelevated(exe: str, params: str = None, cwd: str = None, show: int = 0, wait: bool = False) -> bool | int
```

Allows to run an unelevated exe from an elevated Python process/app.

The unelevated process uses the same security traits as `Explorer`, therefor the function requires `Explorer` to be running (which in Windows is always the case, unless it was deliberately killed).

If `wait=True` is specified, the function returns the exit code (`int`) of the unelevated process, otherwise it returns its process id (`int`).

If some internally used Winapi function fails for whatever reason, an exception is raised that includes the system error code.

The `show` parameter (`int`) specifies if/how the window of the process is displayed, it defaults to 0 (SW_HIDE), i.e. the window is hidden. To show it specify 1 (SW_SHOWNORMAL). See [here](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow) for other possible values.

Usage example:
```python
"""
This example only makes sense if Python was started from an elevated CMD/Terminal,
or if it's part of a frozen Python app that was started elevated.
"""
from elevator import exec_unelevated

# pid = exec_unelevated("cmd.exe", params=r"/c echo foo>D:\foo.txt")

exit_code = exec_unelevated("cmd.exe", params=r"/c echo foo>D:\foo.txt", wait=True)

print(exit_code)
# The created file can be moved or deleted by the user without requiring elevation
```

### 3.) run_elevated_command()

```
run_elevated_command(command_line: str, cwd: str = '') -> tuple[bytes, bytes, int]
```

Allows to run an elevated command from an unelevated Python process/app and return its stdout and stderr output as well as its exit code. The user will get an UAC prompt and has to confirm it.

This might be the *core feature* of this module, since it's the most trickiest one. It's implemented like this:
- A temporary hidden Window is created.
- A new elevated Python process is started, the command to execute as well as the HWND of the hidden window are passed to it via command line.
- The user will get an UAC prompt and has to confirm it.
- The elevated Python process executes the command, and then sends the result - stdout, stderr and exit code - to the temporary hidden window as a WM_COPYDATA window message, and exits.
- The hidden window receives the WM_COPYDATA message, closes the  temporary window and exits its window proc. stdout (`bytes`), stderr (`bytes`) and exit code (`int`) are returned to the calling function/code.

If the user did not confirm the UAC prompt, stdout and stderr are empty and the exit code is 1.

If some internally used Winapi function fails for whatever reason, stdout is empty,  stderr contains an error message that includes the system error code, and the exit code is 2.

Usage example:
```python
from elevator import run_elevated_command

# This directory can only be listed by SYSTEM and Administrators
stdout, stderr, exit_code = run_elevated_command(r"cmd /c dir %windir%\system32\config\systemprofile")

if exit_code == 0:
    print("Result:", stdout.decode("oem"))
else:
    print("Error:", stderr.decode("oem"))
```

### 4.) run_unelevated_command()

```
run_unelevated_command(command_line: str, cwd: str = '') -> tuple[bytes, bytes, int]
```

Allows to run an unelevated command from an elevated Python process/app and return its stdout (`bytes`) and stderr (`bytes`) output as well as its exit code (`int`).

The unelevated command uses the same security traits as `Explorer`, therefor the function requires `Explorer` to be running (which in Windows is always the case, unless it was deliberately killed).

If some internally used Winapi function fails for whatever reason, an exception is raised that includes the system error code.

Usage example:
```python
""" 
This example only makes sense if Python was started from an elevated CMD/Terminal, 
or if it's part of a frozen Python app that was started elevated.
"""
from elevator import run_unelevated_command

# This directory can only be listed by SYSTEM and Administrators,
# so in this case it will fail, even if Python was started from an 
# elevated CMD/Terminal prompt.
stdout, stderr, exit_code = run_unelevated_command(r"cmd /c dir %windir%\system32\config\systemprofile")

if exit_code == 0:
    print("Result:", stdout.decode("oem"))
else:
    print("Error:", stderr.decode("oem"))  # Error: File not found
```
