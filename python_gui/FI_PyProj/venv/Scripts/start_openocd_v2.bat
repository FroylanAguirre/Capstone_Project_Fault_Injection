REM This is an improved version of a previous batch file that could open
REM     Openocd.
REM This improved version can be executed from any directory from Cmd window
REM		assuming that Ac6 directory is in C:
REM Author: Froylan Aguirre

set toOpenocd="Ac6\SystemWorkbench\plugins\fr.ac6.mcu.debug_2.1.1.201708311556\resources\openocd\scripts"
set toOcdExe="C:\Ac6\SystemWorkbench\plugins\fr.ac6.mcu.externaltools.openocd.win32_1.16.0.201708311556\tools\openocd\bin"

cd\
cd %toOpenocd%
%toOcdExe%\openocd.exe -f board\stm32f429discovery.cfg

:NOFINDTERMINAL

