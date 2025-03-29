@echo off
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo Файл requirements.txt не найден!
    pause
)