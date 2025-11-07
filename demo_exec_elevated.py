from elevator import IS_ELEVATED, exec_elevated

print('\nIs Python elevated:', 'yes' if IS_ELEVATED else 'no', '\n')

# pid = exec_elevated("sc.exe", params="stop Spooler")

exit_code = exec_elevated("sc.exe", params="stop Spooler", wait=True)

print('Exit code:', exit_code)  # 0 if spooler service was stopped successfully
