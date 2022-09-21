@echo off


for /F "tokens=2" %%i in ('date /t') do set mydate=%%i
set mytime=%time%
echo Time: %mydate%:%mytime% >> "C:\Users\Korisnik\Desktop\DIPLOMSKI\project\src\app\log_file.txt" 

"C:\Users\Korisnik\AppData\Local\Programs\Python\Python39\pythonw.exe" "C:\Users\Korisnik\Desktop\DIPLOMSKI\project\src\app\main.py" >> "C:\Users\Korisnik\Desktop\DIPLOMSKI\project\src\app\log_file.txt" 

echo ----------------------------------------------------------------- >> "C:\Users\Korisnik\Desktop\DIPLOMSKI\project\src\app\log_file.txt" 

pause

