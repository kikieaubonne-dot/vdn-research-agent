@echo off
setlocal
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set PYTHONDONTWRITEBYTECODE=1
py -3.11 "%~dp0setup.py" doctor
set EPONGE_EXIT=%ERRORLEVEL%
if not "%~1"=="--no-pause" pause
exit /b %EPONGE_EXIT%
