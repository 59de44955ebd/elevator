"""
This example only makes sense if Python was started from an elevated CMD/Terminal,
or if it's part of a frozen Python app that was started elevated.
"""
from elevator import IS_ELEVATED, exec_unelevated

print('\nIs Python elevated:', 'yes' if IS_ELEVATED else 'no', '\n')

# pid = exec_unelevated("cmd.exe", params=r"/c echo foo>D:\foo.txt")

exit_code = exec_unelevated("cmd.exe", params=r"/c echo foo>D:\foo.txt", wait=True)

print('Exit code:', exit_code)

# The created file can be moved or deleted by the user without requiring elevation
