
REM Create build directory and navigate to it
mkdir build
pushd build
REM Enable delayed variable expansion
setlocal enabledelayedexpansion
REM Create a variable to store all .cpp files
set cppFiles=..\main.cpp

REM Add all .cpp files from src to the list
for %%f in (..\src\*.cpp) do (
    set cppFiles=!cppFiles! "%%f"
)


for %%f in (!cppFiles!) do echo %%f

REM Compile the collected files
cl /EHs /W3 /Zi %cppFiles% ^/I "..\include" ^
/I "..\src" ^
/I "C:\Users\Carmel\vclib\C++\SDL2-2.30.5\include" ^
/link /LIBPATH:"C:\Users\Carmel\vclib\C++\SDL2-2.30.5\lib\x64" ^
user32.lib SDL2main.lib SDL2.lib shell32.lib /SUBSYSTEM:CONSOLE

REM Return to the original directory
popd

REM End delayed expansion
endlocal

main.exe > output.txt 2> error.txt
exit