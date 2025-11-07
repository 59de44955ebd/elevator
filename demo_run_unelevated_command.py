"""
This example only makes sense if Python was started from an elevated CMD/Terminal,
or if it's part of a frozen Python app that was started elevated.
"""
from elevator import IS_ELEVATED, run_unelevated_command

print('\nIs Python elevated:', 'yes' if IS_ELEVATED else 'no', '\n')

# This directory can only be listed by SYSTEM and Administrators,
# so in this case it will fail, even if Python was started from an
# elevated CMD/Terminal prompt.
stdout, stderr, exit_code = run_unelevated_command(r"cmd /c dir %windir%\system32\config\systemprofile")

if exit_code == 0:
    print("Result:", stdout.decode("oem"))
else:
    print("Error:", stderr.decode("oem"))  # Error: File not found
