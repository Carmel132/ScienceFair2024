@echo off
set ScriptDir=%~dp0

REM Launch a new console with Visual Studio environment variables set
start "" cmd.exe /k ""C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat" x64 && cd /d %ScriptDir% && call compile.bat build> build/compile.txt"

REM Exit this script to avoid running commands in the current shell
exit
