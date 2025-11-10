set pyv=%UserProfile%\AppData\Local\Programs\Python\Python39\
set py=%pyv%\python.exe

set name=venv

:: %py% -V && ( pause ) || ( pause )
%py% -m venv %name% && ( pause ) || ( pause )
