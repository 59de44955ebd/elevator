@echo off
setlocal EnableDelayedExpansion
cd /d %~dp0

REM Config
set APP_NAME=demo_app
set DIR=%CD%
set APP_DIR=%CD%\dist\%APP_NAME%\

REM Cleanup dist folder
rmdir /s /q "dist\%APP_NAME%" 2>nul

echo.
echo ****************************************
echo Running pyinstaller...
echo ****************************************
pyinstaller --noupx -w -i "app.ico" -n "%APP_NAME%" -D main.py

echo.
echo ****************************************
echo Optimizing dist folder...
echo ****************************************

del "dist\%APP_NAME%\_internal\api-ms-win-*.dll"
del "dist\%APP_NAME%\_internal\_socket.pyd"
del "dist\%APP_NAME%\_internal\libcrypto-3.dll"
del "dist\%APP_NAME%\_internal\select.pyd"

call :create_7z

:done
echo.
echo ****************************************
echo Done.
echo ****************************************
echo.
pause

endlocal
goto :eof


:create_7z
if not exist "C:\Program Files\7-Zip\" (
	echo.
	echo ****************************************
	echo 7z.exe not found at default location, omitting .7z creation...
	echo ****************************************
	exit /B
)
echo.
echo ****************************************
echo Creating .7z archive...
echo ****************************************
cd dist
set PATH=C:\Program Files\7-Zip;%PATH%
7z a "%APP_NAME%-windows-x64.7z" "%APP_NAME%\*"
cd ..
exit /B
