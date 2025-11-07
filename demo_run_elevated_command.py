from elevator import run_elevated_command

# This directory can only be listed by SYSTEM and Administrators
stdout, stderr, exit_code = run_elevated_command(r"cmd /c dir %windir%\system32\config\systemprofile")

if exit_code == 0:
    print("Result:", stdout.decode("oem"))
else:
    print("Error:", stderr.decode("oem"))
