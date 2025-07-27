@echo off
title Генератор паролей
color 0A

REM Если у вас портативная версия Python
set PYTHON_PATH=pythonpython.exe

if exist %PYTHON_PATH% (
    echo Используется портативная версия Python
    %PYTHON_PATH% password_generator.py
) else (
    echo Используется системный Python
    python password_generator.py
)

pause