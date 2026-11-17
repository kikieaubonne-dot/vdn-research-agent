@echo off
setlocal
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set PYTHONDONTWRITEBYTECODE=1
py -3.11 -B "%~dp0..\Eponge\source\vdn_mcp.py" --root "%~dp0..\Eponge\runtime" --v112
exit /b %ERRORLEVEL%
