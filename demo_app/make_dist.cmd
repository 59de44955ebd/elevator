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

:done
echo.
echo ****************************************
echo Done.
echo ****************************************
echo.
pause
