@echo off
@title


::if exist Read_file (
::	echo "file is elready existed"
::) else (
::	md Read_file
::	echo "bulid file"
::)

if not exist Read_file md Read_file

::jlink>jlink.txt
::set LIST = 123

"C:\Program Files (x86)\SEGGER\JLink_V632h\JLink.exe" -device AMAPH1KK-KBR -SelectEmuBySN 59405067 -if swd -commanderscript "readAddr.jlink">read.txt

if not exist readbin.txt echo.>readbin.txt

type read.txt >> readbin.txt

type readbin.txt | findstr /v S | findstr /v D | findstr /v J | findstr /v R | findstr /v P | findstr /v o | findstr /v r | findstr /v "^$">userData.txt



del read.txt
copy userData.txt Read_file 
::del readbin.txt 
del userData.txt 

::pause
exit 



