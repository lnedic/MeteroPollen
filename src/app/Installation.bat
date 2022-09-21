@echo off
"C:\Users\Korisnik\AppData\Local\Programs\Python\Python39\python.exe" "C:\Users\Korisnik\Desktop\DIPLOMSKI\project\src\installation.py"

:choice
set /P c=Do you want to continue [Y/N]?
if /I "%c%" EQU "Y" goto :yes
if /I "%c%" EQU "N" goto :no
goto :choice


:yes
set /p city="Unesite ime grada za koji zelite ucitati povijesne podatke u bazu: "
echo Prikupljam povijesne podatke za grad: %city%
"C:\Users\Korisnik\AppData\Local\Programs\Python\Python39\python.exe"  "C:\Users\Korisnik\Desktop\DIPLOMSKI\project\src\History_main.py" %city% yes
goto :continue

:no
exit no

:continue
pause 
exit

rem create task ni task sceduler to run script for sync data
REM SCHTASKS /CREATE /SC DAILY /TN "MyTasks\Sync Pollen Data 2" /TR "C:\Users\Korisnik\Desktop\DIPLOMSKI\project\src\main.bat" /ST 16:00


