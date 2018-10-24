@echo off

if not exist read.txt echo.>read.txt

"C:\Program Files (x86)\SEGGER\JLink_V632h\JLink.exe" -device AMAPH1KK-KBR -SelectEmuBySN 59405067 -if swd -commanderscript "readAddr.jlink">read_flash.txt
::"C:\Program Files\SEGGER\JLink_V622e\JLink.exe" -device AMAPH1KK-KBR -SelectEmuBySN 59407735 -if swd -commanderscript "readAddr.jlink">read_flash.txt

if not exist Read_Nfc md Read_Nfc
type read_flash.txt >> read.txt

FINDSTR "000FF8DC" read.txt>nul
if %errorlevel% equ 0 (
	type read.txt >> readbin.txt
	copy readbin.txt Read_Nfc 
	echo Success.
) else (
	echo Failure.
)
del read.txt
del read_flash.txt

::exit 
pause



