@echo off
setlocal
cd /d "%~dp0"
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
if not "%~1"=="" goto command
echo L'Eponge - noyau borne, sans installation de service
echo 1. Diagnostic
echo 2. Etat
echo 3. Bilan
echo 4. Arreter
echo 5. Preparer une NOUVELLE mission isolee
echo 6. Demarrer la mission preparee, hors ligne
set /p EPONGE_CHOICE=Choix :
if "%EPONGE_CHOICE%"=="1" py -3.11 eponge.py doctor
if "%EPONGE_CHOICE%"=="2" py -3.11 eponge.py status
if "%EPONGE_CHOICE%"=="3" py -3.11 eponge.py report
if "%EPONGE_CHOICE%"=="4" py -3.11 eponge.py stop
if "%EPONGE_CHOICE%"=="5" py -3.11 eponge.py init
if "%EPONGE_CHOICE%"=="6" py -3.11 eponge.py start --activate
pause
exit /b
:command
py -3.11 "%~dp0eponge.py" %*
exit /b %ERRORLEVEL%
