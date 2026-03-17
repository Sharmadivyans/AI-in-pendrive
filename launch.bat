@echo off
title Portable AI Loader
color 0A
cls

:: Get the current drive letter (e.g., E:\)
set DRIVE=%~dp0

:: Set the path to the portable Python executable
:: IMPORTANT: Change "python-3.10.11.amd64" to match the actual folder name inside your /env folder on your physical USB!
set PYTHON_EXE=%DRIVE%env\python-3.10.11.amd64\python.exe

:: Launch the main AI script
echo ========================================
echo   PORTABLE AI SYSTEM INITIALIZING...
echo ========================================
echo.
echo Launching from: %DRIVE%
echo.

"%PYTHON_EXE%" "%DRIVE%jarvis.py"

pause
