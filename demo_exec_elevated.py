from elevator import exec_elevated

# pid = exec_elevated("sc.exe", params="stop Spooler")

exit_code = exec_elevated("sc.exe", params="stop Spooler", wait=True)

print(exit_code)  # 0 if spooler service was stopped successfully
