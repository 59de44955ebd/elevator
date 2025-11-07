from elevator import IS_ELEVATED, run_elevated_command

if __name__ == '__main__':

    print('\nIs Python elevated:', 'yes' if IS_ELEVATED else 'no', '\n')

    # This directory can only be listed by SYSTEM and Administrators
    stdout, stderr, exit_code = run_elevated_command(r"cmd /c dir %windir%\system32\config\systemprofile")

    if exit_code == 0:
        print("Result:", stdout.decode("oem"))
    else:
        print("Error:", exit_code, stderr.decode("oem"))
