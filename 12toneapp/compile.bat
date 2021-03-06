@echo off

set /p last_v="Enter last version number: "
set /p curr_v="Enter new version number: "

copy main.py pys\v%curr_v%.py
if exist latest.exe copy latest.exe exes\v%last_v%.exe
pyinstaller --onefile -w main.py
copy dist\main.exe latest.exe
copy latest.exe exes\v%curr_v%.exe
rmdir /s /q dist
rmdir /s /q build
rmdir /s /q __pycache__
del main.spec